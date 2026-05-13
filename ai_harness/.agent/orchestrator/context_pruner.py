import os
import subprocess
import json
import ntpath
from context_map_validator import ContextMapValidator

def _portable_basename(path):
    """Return a filename for either POSIX or Windows-style paths."""
    value = str(path or "")
    return os.path.basename(ntpath.basename(value))


class ContextPruner:
    def __init__(self, config, workspace_root):
        self.config = config
        self.workspace_root = workspace_root
        self.context_map_validator = ContextMapValidator(workspace_root)

    def build_context_pack(self, feature_slug, stage, user_request, state):
        pack_path = os.path.join(
            self.workspace_root,
            self.config["paths"]["loop_flow"],
            "context_packs",
            f"{feature_slug}_{stage}_context.md"
        )
        os.makedirs(os.path.dirname(pack_path), exist_ok=True)

        search_terms = self.build_search_terms(state, stage)
        
        print(f"Pruning context with terms: {search_terms}")
        culler_output = self.run_culler(search_terms)

        # Filter artifacts to only include current feature slug
        all_artifacts = state.get('artifacts', {})
        relevant_artifacts = all_artifacts

        # Filter source context to exclude orchestrator internals and generated/noisy
        # files for game development.
        is_harness = state.get("stack_profile") == "harness_internal"
        if not is_harness:
            harness_dirs = [
                ".agent/orchestrator", ".agent/skills", ".agent/workflows",
                ".agent/bin", ".agent/scratch", ".agent/logs", ".agent/state",
                "tests", "tools", "ui/", "logs/", "scratch/"
            ]
            noisy_files = [
                "ai_harness_bundle.txt", "debug_prompt.txt", "package-lock.json",
                "kobold.log", "orchestrator_ui.log", "loop_central.log", "generations.jsonl",
                "__pycache__", ".pyc"
            ]
            culler_lines = culler_output.splitlines()
            filtered_lines = []
            for line in culler_lines:
                if any(h_dir in line for h_dir in harness_dirs):
                    continue
                if any(noisy in line for noisy in noisy_files):
                    continue
                filtered_lines.append(line)
            culler_output = "\n".join(filtered_lines)

        artifact_content = self._get_artifact_content(relevant_artifacts)

        # Include Target Files from context_map fully
        target_files_content, context_map_validation = self._get_target_files_content(
            relevant_artifacts,
            state,
            f"{state.get('feature', '')}\n\n{artifact_content}",
        )

        content = f"""# Context Pack: {feature_slug} / {stage}

## Feature Goal
{state.get('feature')}

## Current Stage
{stage}

## Decision Memory
Refer to .agent/Loop_Flow/context_packs/{feature_slug}_decision_memory.md for stable decisions and constraints.

## Relevant Artifacts
{json.dumps(relevant_artifacts, indent=2)}

## Target Source Files
These source files are already available in this context. Do not request research just to read them; proceed with the stage using this evidence.

{target_files_content}

## Context Map Validation
{context_map_validation}

## Artifact Content
{artifact_content}

## Relevant Research Briefs
{self._get_research_context(state)}

## Validation Status
{json.dumps((state.get('last_validation') or {}).get('errors', []), indent=2)}

## Pruned Source Context
{culler_output}
"""
        with open(pack_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return pack_path

    def build_search_terms(self, state, stage):
        # 1. Improved Keyword Extraction
        search_terms = []
        # From feature description
        search_terms.extend(state.get("feature", "").split()[:15])
        # From current stage needs
        search_terms.append(stage)
        # From recent research. Use concise metadata only; full absolute artifact
        # paths create noisy Windows path tokens that hurt model compliance.
        for brief in state.get("research_briefs", [])[-2:]:
            search_terms.extend(_portable_basename(brief).split()[:10])
        for result in state.get("research_results", [])[-4:]:
            if result.get("status") not in ("complete", "partial", "sufficient"):
                continue
            search_terms.extend(str(result.get("query", "")).split()[:10])
            search_terms.extend(str(result.get("status", "")).split()[:3])
            search_terms.extend(_portable_basename(result.get("artifact_path", "")).split()[:5])
            for tag in result.get("topic_tags", [])[:5]:
                search_terms.extend(str(tag).split()[:3])
            title = result.get("title") or result.get("brief_title") or result.get("summary", "")
            search_terms.extend(str(title).split()[:10])
        # From validation failures
        if state.get("last_validation") and not state["last_validation"]["valid"]:
            for err in state["last_validation"]["errors"]:
                search_terms.extend(err.split()[:5])
        
        # Dedupe and clean
        cleaned_terms = []
        seen = set()
        for term in search_terms:
            cleaned = str(term).lower().strip(",.()\"")
            if len(cleaned) <= 3:
                continue
            if os.path.isabs(cleaned) or ":\\" in cleaned or ":/" in cleaned:
                cleaned = _portable_basename(cleaned)
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            cleaned_terms.append(cleaned)
        return cleaned_terms[:20]

    def run_culler(self, keywords):
        try:
            cmd = ["python", "tools/context_culler.py"] + keywords
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)
            return result.stdout if result.returncode == 0 else "Culler failed."
        except Exception as e:
            return f"Culler error: {str(e)}"
        
    def _get_research_context(self, state):
        results = state.get("research_results", [])
        if not results:
            return "No research results available yet."
            
        research_content = ""
        usable_results = [
            res for res in results
            if res.get("status") in ("complete", "partial", "sufficient")
        ]
        stale_results = [
            res for res in results
            if res.get("status") not in ("complete", "partial", "sufficient")
        ]

        if not usable_results:
            if stale_results:
                return (
                    "No complete research results available. Recent blocked research is omitted "
                    "from evidence because it may be stale or contradicted by provided target files."
                )
            return "No research results available yet."

        for res in usable_results[-3:]: # Include last 3 useful results
            title = res.get("title") or res.get("brief_title") or res.get("query", "Unknown Research")
            status = res.get("status", "unknown")
            artifact = _portable_basename(res.get("artifact_path", "N/A"))
            
            research_content += f"### {title}\n"
            research_content += f"- Status: {status}\n"
            research_content += f"- Artifact: {artifact}\n"
            
            findings = res.get("findings", [])
            if findings:
                research_content += "- Key Findings:\n"
                for f in findings[:2]: # Top 2 findings
                    # Stricter snippet to avoid prompt bloat
                    text = str(f).strip()
                    if len(text) > 150:
                        text = text[:150] + "..."
                    research_content += f"  - {text}\n"
            research_content += "\n"
        return research_content

    def generate_slug(self, text):
        import re
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9 ]', '', slug)
        slug = slug.replace(' ', '_')
        return slug[:48]

    def _get_artifact_content(self, artifacts):
        if not artifacts:
            return "No artifacts available."
        
        content = ""
        max_total_chars = self.config.get("context_budget", {}).get("active_artifact_chars", 12000)
        total_chars = 0
        for name, path in artifacts.items():
            if not name.endswith('.md') and not name.endswith('.json'):
                continue
            
            full_path = os.path.join(self.workspace_root, path) if not os.path.isabs(path) else path
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        file_text = f.read()
                        remaining = max_total_chars - total_chars
                        if remaining <= 0:
                            content += "\n... [additional artifact content omitted by context budget] ...\n"
                            break
                        if len(file_text) > remaining:
                            file_text = file_text[:remaining] + "\n... [TRUNCATED] ..."
                        block = f"### Artifact: {name}\n```\n{file_text}\n```\n\n"
                        content += block
                        total_chars += len(block)
                except Exception as e:
                    content += f"### Artifact: {name} (Error reading: {str(e)})\n\n"
        return content or "No readable markdown/JSON artifact content found."

    def _get_target_files_content(self, artifacts, state=None, candidate_text=""):
        context_map_path = artifacts.get("context_map.json")
        if not context_map_path:
            return "No context_map.json available to identify target files.", "No context map was available."
        
        full_map_path = os.path.join(self.workspace_root, context_map_path) if not os.path.isabs(context_map_path) else context_map_path
        if not os.path.exists(full_map_path):
            return f"Context map not found at {full_map_path}", f"ERROR: Context map not found at {full_map_path}"
            
        try:
            validation = self.context_map_validator.validate_file(
                context_map_path,
                stack_profile=(state or {}).get("stack_profile", "game_source"),
                candidate_text=candidate_text,
                repair=True,
            )
            
            target_files = validation.target_files
            if not target_files:
                return "No target_files listed in context_map.json.", self._format_context_map_validation(validation)
                
            total_chars = 0
            max_total_chars = self.config.get("context_budget", {}).get("target_source_chars", 18000)
            
            content = ""
            for tf in target_files:
                if total_chars >= max_total_chars:
                    content += f"\n... [ADDITIONAL TARGET FILES OMITTED TO SAVE CONTEXT] ...\n"
                    break
                    
                path = tf.get("path") if isinstance(tf, dict) else tf
                if not path: continue
                
                full_path = os.path.join(self.workspace_root, path)
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_text = f.read()
                        
                        # Aggressive per-file truncation
                        file_limit = 8000
                        if len(file_text) > file_limit:
                            file_text = file_text[:file_limit] + "\n... [TRUNCATED] ..."
                        
                        file_block = f"### Target File: {path}\n```\n{file_text}\n```\n\n"
                        content += file_block
                        total_chars += len(file_block)
                else:
                    content += f"### Target File: {path} (NOT FOUND)\n\n"
            return content or "No target files could be read.", self._format_context_map_validation(validation)
        except Exception as e:
            return f"Error reading target files from context map: {str(e)}", f"ERROR: {str(e)}"

    def _format_context_map_validation(self, validation):
        status = "valid" if validation.valid else "invalid"
        lines = [f"- Status: {status}", f"- Target files: {len(validation.target_files)}"]
        if validation.changed:
            lines.append("- Normalized: yes")
        for warning in validation.warnings[:5]:
            lines.append(f"- Warning: {warning}")
        for error in validation.errors[:8]:
            lines.append(f"- Error: {error}")
        return "\n".join(lines)
