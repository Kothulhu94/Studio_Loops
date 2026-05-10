import os
import subprocess
import json
import ntpath

def _portable_basename(path):
    """Return a filename for either POSIX or Windows-style paths."""
    value = str(path or "")
    return os.path.basename(ntpath.basename(value))


class ContextPruner:
    def __init__(self, config, workspace_root):
        self.config = config
        self.workspace_root = workspace_root

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
        relevant_artifacts = {k: v for k, v in all_artifacts.items() if feature_slug in k or "common" in k}

        content = f"""# Context Pack: {feature_slug} / {stage}

## Feature Goal
{state.get('feature')}

## Current Stage
{stage}

## Decision Memory
Refer to .agent/Loop_Flow/context_packs/{feature_slug}_decision_memory.md for stable decisions and constraints.

## Relevant Artifacts
{json.dumps(relevant_artifacts, indent=2)}

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
        for result in state.get("research_results", [])[-2:]:
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
        for res in results[-3:]: # Include last 3 results
            title = res.get("title") or res.get("brief_title") or res.get("query", "Unknown Research")
            status = res.get("status", "unknown")
            artifact = _portable_basename(res.get("artifact_path", "N/A"))
            
            research_content += f"### {title}\n"
            research_content += f"- Status: {status}\n"
            research_content += f"- Artifact: {artifact}\n"
            
            findings = res.get("findings", [])
            if findings:
                research_content += "- Key Findings:\n"
                for f in findings[:3]: # Top 3 findings
                    research_content += f"  - {str(f)[:200]}\n"
            research_content += "\n"
        return research_content

    def generate_slug(self, text):
        import re
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9 ]', '', slug)
        slug = slug.replace(' ', '_')
        return slug[:48]
