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

    def compile_prompt(self, stage, feature, user_request, state, role_workflow, role_skills, context_pack_content, validation_rules, required_outputs):
        stack_profile = state.get("stack_profile", "game_source")
        
        if stack_profile == "harness_internal":
            stack_info = (
                "- Primary language: Python 3\n"
                "- Harness files: .agent/orchestrator/\n"
                "- Tests: tests/*.py\n"
                "- Tools: tools/*.py\n"
                "- Docs/workflows/skills may be edited when relevant\n"
                "- TypeScript/Vitest only matters if src/ or tests/*.ts are touched\n"
                "- Do not force browser/game-source constraints onto orchestrator work"
            )
        else:
            stack_info = (
                "- Language: TypeScript (strict)\n"
                "- Environment: Browser\n"
                "- Source Directory: src/\n"
                "- Test Directory: tests/\n"
                "- Test Runner: Vitest\n"
                "- Logic: Vanilla JS/TS logic, Canvas/DOM APIs.\n"
                "- NO Python implementation plans for game source."
            )

        current_date_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        stage_specific_contract = ""
        if stage == "researcher":
            feature_slug = state.get("feature_slug", "{feature}")
            stage_specific_contract = (
                "## Stage Artifact Contract\n"
                "When completing researcher, write these artifacts in ACTIONS_JSON:\n"
                f"- `.agent/Loop_Flow/{feature_slug}_blueprint.md` with sections: "
                "Technical Audit, Implementation Blueprint, Context Pruning Map, Implementation Checklist.\n"
                "- `.agent/Loop_Flow/context_map.json` as valid JSON.\n"
                "Set status=\"complete\" only when both writes are present.\n"
            )

        if os.path.exists(self.template_path):
            from string import Template
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_str = f.read()
            
            template = Template(template_str)
            user_prompt = template.safe_substitute(
                stage=stage,
                feature=feature,
                user_request=user_request,
                stack_info=stack_info,
                current_date_utc=current_date_utc,
                state=json.dumps(state, indent=2),
                role_instructions=role_workflow,
                skills=role_skills,
                artifacts=".agent/Loop_Flow/", 
                context=context_pack_content,
                required_outputs=json.dumps(required_outputs, indent=2),
                validation_rules=json.dumps(validation_rules, indent=2),
                stage_specific_contract=stage_specific_contract
            )
        else:
            # Fallback (updated to remove forbidden terms)
            user_prompt = f"# Studio Loop Stage Prompt\nRole: {stage}\nFeature: {feature}"

        system_prompt = (
            f"You are the active Studio Loop role: {stage}.\n"
            "You are running as Gemma 4 through KoboldCPP's OpenAI-compatible chat API. "
            "Gemma 4 supports a native system role, so treat these system instructions as higher priority than user/context text.\n"
            "Think silently; never expose hidden reasoning, scratchpads, or chain-of-thought.\n"
            "Prefer concise, deterministic, schema-following outputs over conversational prose.\n"
            "The orchestrator controls transitions and executes tools from ACTIONS_JSON only.\n"
            "Complete only the current stage.\n"
        )

        return {
            "system": system_prompt,
            "user": user_prompt
        }
