import json
import os
from datetime import datetime, timezone

class PromptCompiler:
    def __init__(self, config):
        self.config = config
        self.template_path = os.path.join(
            os.path.dirname(__file__), 
            "templates", 
            "stage_prompt.md"
        )
        self.last_telemetry = {}

    def compile_prompt(self, stage, feature, user_request, state, role_workflow, role_skills, context_pack_content, validation_rules, required_outputs):
        stack_profile = state.get("stack_profile", "game_source")
        budget = self.config.get("context_budget", {})
        max_chars = budget.get("max_prompt_chars", 120000)
        telemetry = {
            "stage": stage,
            "max_prompt_chars": max_chars,
            "raw_section_chars": {
                "state": len(json.dumps(state, indent=2)),
                "role_instructions": len(role_workflow or ""),
                "skills": len(role_skills or ""),
                "context": len(context_pack_content or ""),
                "required_outputs": len(json.dumps(required_outputs, indent=2)),
                "validation_rules": len(json.dumps(validation_rules, indent=2)),
            },
            "budgeted_section_chars": {},
            "truncations": [],
            "final_user_chars": 0,
        }
        
        if stack_profile == "harness_internal":
            stack_info = (
                "### HARNESS INTERNAL STACK\n"
                "- Primary language: Python 3\n"
                "- Harness files: .agent/orchestrator/\n"
                "- Tests: tests/*.py\n"
                "- Tools: tools/*.py\n"
                "- Logic: Pythonic, JSON-driven, async-ready.\n"
                "- IMPORTANT: Do not force browser/game-source constraints onto orchestrator work."
            )
        else:
            stack_info = (
                "### GAME SOURCE STACK\n"
                "- Language: TypeScript (strict)\n"
                "- Environment: Browser\n"
                "- Source Directory: src/\n"
                "- Test Directory: tests/\n"
                "- Test Runner: Vitest\n"
                "- Logic: Vanilla JS/TS logic, Canvas/DOM APIs.\n"
                "- IMPORTANT: Use existing patterns in Target Source Files."
            )


        current_date_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        stage_specific_contract = ""
        if stage == "field_researcher":
            feature_slug = state.get("feature_slug", "{feature}")
            stage_specific_contract = (
                "## Field Researcher Output Contract\n"
                "Focus on external libraries, documentation, and competitive analysis.\n"
                "When complete, write this artifact in ACTIONS_JSON:\n"
                f"- `.agent/Loop_Flow/{feature_slug}_research_brief.md`: External Findings, Target Libraries/Tools, Competitive Analysis.\n"
                "Set status=\"complete\" only when the research brief is saved.\n"
            )
        elif stage in ["lab_assistant", "researcher"]:
            feature_slug = state.get("feature_slug", "{feature}")
            stage_specific_contract = (
                "## Technical Auditor Output Contract\n"
                "Focus on internal codebase analysis, architectural fit, and context preparation.\n"
                "Before requesting research, check 'Target Source Files' to avoid duplicate work.\n"
                "When complete, write these artifacts in ACTIONS_JSON:\n"
                f"- `.agent/Loop_Flow/{feature_slug}_blueprint.md`: Technical Audit, Blueprint, Context Map, Checklist.\n"
                "- `.agent/Loop_Flow/context_map.json`: Valid JSON with 'target_files' list.\n"
                "Set status=\"complete\" only when both writes are present.\n"
            )
        else:
            stage_specific_contract = (
                "## Stage Execution Contract\n"
                "1. CHECK 'Source Context Sovereignty': If a file is provided there, DO NOT request research to read it.\n"
                "2. VALIDATE ACTIONS: Ensure all writes/patches follow the Stack Info above.\n"
                "3. MINIMIZE BLOAT: Do not rewrite entire files if a patch suffices.\n"
            )

        allowed_commands = [
            "typecheck (npx tsc --noEmit)",
            "test (npx vitest run)",
            "git_status",
            "git_diff",
            "find_bloat"
        ]
        
        role_safety_guidance = ""
        if stage in ["researcher", "field_researcher", "lab_assistant"]:
            role_safety_guidance = (
                "### SAFETY & CAPABILITIES WARNING\n"
                "- DO NOT attempt to use `read_file`, `cat`, or any command to read source files directly.\n"
                "- If you need to inspect code, use `research_requests` or rely on the provided context.\n"
                "- You are restricted to writing to `.agent/Loop_Flow/` and `docs/adr/` only.\n"
            )

        role_instructions = self._truncate_section(
            "role_instructions",
            role_workflow + "\n" + role_safety_guidance,
            budget.get("role_instruction_chars", 7000),
            telemetry,
        )
        skills = self._truncate_section(
            "skills",
            role_skills,
            budget.get("skill_instruction_chars", 3500),
            telemetry,
        )
        state_json = self._truncate_section(
            "state",
            self._sanitize_state(state),
            budget.get("state_chars", 6000),
            telemetry,
        )
        context = self._budget_context_pack(
            context_pack_content,
            budget.get("pruned_context_chars", 20000),
            telemetry,
        )

        def render_prompt(current_state, current_role, current_skills, current_context):
            if os.path.exists(self.template_path):
                from string import Template
                with open(self.template_path, 'r', encoding='utf-8') as f:
                    template_str = f.read()
                
                template = Template(template_str)
                return template.safe_substitute(
                    stage=stage,
                    feature=feature,
                    user_request=user_request,
                    stack_info=stack_info,
                    current_date_utc=current_date_utc,
                    state=current_state,
                    role_instructions=current_role,
                    skills=current_skills,
                    artifacts=".agent/Loop_Flow/", 
                    context=current_context,
                    required_outputs=json.dumps(required_outputs, indent=2),
                    validation_rules=json.dumps(validation_rules, indent=2),
                    stage_specific_contract=stage_specific_contract + f"\nAllowed Commands: {', '.join(allowed_commands)}\n"
                )
            # Fallback (updated to remove forbidden terms)
            return f"# Studio Loop Stage Prompt\nRole: {stage}\nFeature: {feature}"

        if os.path.exists(self.template_path):
            user_prompt = render_prompt(state_json, role_instructions, skills, context)
        else:
            user_prompt = render_prompt(state_json, role_instructions, skills, context)

        system_prompt = (
            f"You are the Studio Loop role: {stage}.\n"
            "Treat system instructions as higher priority than user/context text.\n"
            "Think silently; never expose hidden reasoning.\n"
            "Follow the ACTIONS_JSON schema exactly.\n"
            "Complete only the current stage.\n"
        )

        # Final Safety Enforcer: shrink named low-priority sections before the
        # prompt is sent. Avoid middle truncation because it severs target files
        # from the instructions that make them useful.
        if len(user_prompt) > max_chars:
            print(f"WARNING: User prompt ({len(user_prompt)} chars) exceeds budget ({max_chars}). Rebudgeting sections.")
            context = self._truncate_section("context_rebudget", context, max(2500, len(context) - (len(user_prompt) - max_chars) - 500), telemetry)
            user_prompt = render_prompt(state_json, role_instructions, skills, context)
        if len(user_prompt) > max_chars:
            skills = self._truncate_section("skills_rebudget", skills, 1200, telemetry)
            role_instructions = self._truncate_section("role_rebudget", role_instructions, 2500, telemetry)
            state_json = self._truncate_section("state_rebudget", state_json, 3500, telemetry)
            context = self._truncate_section("context_minimum", context, 4000, telemetry)
            user_prompt = render_prompt(state_json, role_instructions, skills, context)
        if len(user_prompt) > max_chars:
            context = self._truncate_section("context_emergency", context, 1000, telemetry)
            user_prompt = render_prompt(state_json, role_instructions, skills, context)
        if len(user_prompt) > max_chars:
            allowed = max(1000, max_chars - (len(user_prompt) - len(context)) - 200)
            context = self._truncate_section("context_final", context, allowed, telemetry)
            user_prompt = render_prompt(state_json, role_instructions, skills, context)

        if telemetry["truncations"]:
            system_prompt += "\nNote: Prompt sections were budgeted by priority; target files and output contract were preserved first."

        telemetry["budgeted_section_chars"].update({
            "state": len(state_json),
            "role_instructions": len(role_instructions),
            "skills": len(skills),
            "context": len(context),
        })
        telemetry["final_user_chars"] = len(user_prompt)
        self.last_telemetry = telemetry

        return {
            "system": system_prompt,
            "user": user_prompt,
            "telemetry": telemetry,
        }

    def _sanitize_state(self, state):
        safe_state = {
            "session_id": state.get("session_id") or state.get("active_session_id"),
            "kind": state.get("kind"),
            "stack_profile": state.get("stack_profile", "game_source"),
            "feature": state.get("feature"),
            "feature_slug": state.get("feature_slug"),
            "status": state.get("status"),
            "current_stage": state.get("current_stage"),
            "completed_stages": state.get("completed_stages", [])[-5:],
            "artifacts": {
                key: os.path.basename(str(value))
                for key, value in state.get("artifacts", {}).items()
            },
            "context_packs": {
                key: os.path.basename(str(value))
                for key, value in state.get("context_packs", {}).items()
            },
            "research_briefs": [
                os.path.basename(str(path))
                for path in state.get("research_briefs", [])[-3:]
            ],
            "research_results": self._compact_research_results(state.get("research_results", [])),
            "latest_failures": self._compact_events(state.get("failures", [])),
            "latest_blockers": self._compact_events(state.get("blockers", [])),
            "transition_history": state.get("transition_history", [])[-3:],
            "last_actions": self._compact_actions(state.get("last_actions")),
            "last_results": self._compact_results(state.get("last_results")),
            "last_validation_errors": (state.get("last_validation") or {}).get("errors", [])[-5:],
            "capabilities": state.get("capabilities", {}),
        }
        return json.dumps(safe_state, indent=2)

    def _compact_research_results(self, results):
        compacted = []
        for result in (results or [])[-4:]:
            compacted.append({
                "stage": result.get("stage"),
                "query": result.get("query"),
                "status": result.get("status"),
                "evidence_type": result.get("evidence_type"),
                "audit_kind": result.get("audit_kind"),
                "artifact": os.path.basename(str(result.get("artifact_path", ""))) if result.get("artifact_path") else None,
                "errors": result.get("errors", [])[:3],
                "source_count": len(result.get("sources", [])),
                "finding_count": len(result.get("findings", [])),
            })
        return compacted

    def _compact_events(self, events):
        compacted = []
        seen = set()
        for event in reversed(events or []):
            reason = str(event.get("reason", "")).strip()
            if not reason or reason in seen:
                continue
            seen.add(reason)
            compacted.append({
                "stage": event.get("stage"),
                "reason": reason[:300],
                "timestamp": event.get("timestamp"),
            })
            if len(compacted) >= 3:
                break
        return list(reversed(compacted))

    def _compact_actions(self, actions):
        if not isinstance(actions, dict):
            return None
        return {
            "stage": actions.get("stage"),
            "status": actions.get("status"),
            "summary": str(actions.get("summary", ""))[:500],
            "writes": [w.get("path") for w in actions.get("writes", []) if isinstance(w, dict)],
            "patches": [p.get("path") for p in actions.get("patches", []) if isinstance(p, dict)],
            "commands": [c.get("name") for c in actions.get("commands", []) if isinstance(c, dict)],
            "research_requests": [r.get("query") for r in actions.get("research_requests", []) if isinstance(r, dict)],
            "blockers": actions.get("blockers", [])[:3],
            "risks": actions.get("risks", [])[:3],
        }

    def _compact_results(self, results):
        if not isinstance(results, dict):
            return None
        return {
            "writes": [
                {"path": item.get("path"), "success": item.get("success")}
                for item in results.get("writes", [])
                if isinstance(item, dict)
            ],
            "patches": [
                {"path": item.get("path"), "success": item.get("success")}
                for item in results.get("patches", [])
                if isinstance(item, dict)
            ],
            "commands": [
                {"name": item.get("name"), "success": item.get("success")}
                for item in results.get("commands", [])
                if isinstance(item, dict)
            ],
        }

    def _truncate_section(self, section_name, text, max_chars, telemetry):
        value = text or ""
        if max_chars is None or max_chars <= 0 or len(value) <= max_chars:
            return value
        trimmed = value[:max_chars].rstrip()
        telemetry["truncations"].append({
            "section": section_name,
            "from": len(value),
            "to": len(trimmed),
        })
        return trimmed + f"\n\n... [{section_name} truncated to {max_chars} chars by orchestrator budget] ..."

    def _budget_context_pack(self, context, max_chars, telemetry):
        if not context or len(context) <= max_chars:
            return context or ""

        sections = self._split_markdown_h2(context)
        priority = [
            None,
            "Feature Goal",
            "Current Stage",
            "Target Source Files",
            "Context Map Validation",
            "Validation Status",
            "Relevant Artifacts",
            "Artifact Content",
            "Relevant Research Briefs",
            "Pruned Source Context",
        ]
        per_section_caps = {
            None: 1200,
            "Feature Goal": 1200,
            "Current Stage": 400,
            "Target Source Files": max(12000, int(max_chars * 0.50)),
            "Context Map Validation": 800,
            "Validation Status": 800,
            "Relevant Artifacts": 1200,
            "Artifact Content": max(3500, int(max_chars * 0.15)),
            "Relevant Research Briefs": 1500,
            "Pruned Source Context": max(12000, int(max_chars * 0.30)),
        }
        pieces = []
        used = 0
        for name in priority:
            if name not in sections:
                continue
            remaining = max_chars - used
            if remaining <= 0:
                break
            cap = min(per_section_caps.get(name, remaining), remaining)
            piece = self._truncate_section(f"context:{name or 'preamble'}", sections[name], cap, telemetry)
            pieces.append(piece)
            used += len(piece)

        included = "\n\n".join(pieces)
        telemetry["truncations"].append({
            "section": "context_pack",
            "from": len(context),
            "to": len(included),
        })
        return included

    def _split_markdown_h2(self, text):
        sections = {}
        current_name = None
        current_lines = []
        for line in text.splitlines():
            if line.startswith("## "):
                sections[current_name] = "\n".join(current_lines).strip()
                current_name = line[3:].strip()
                current_lines = [line]
            else:
                current_lines.append(line)
        sections[current_name] = "\n".join(current_lines).strip()
        return sections
