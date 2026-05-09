import os
import subprocess
import json

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

        # 1. Improved Keyword Extraction
        search_terms = []
        # From feature description
        search_terms.extend(state.get("feature", "").split()[:15])
        # From current stage needs
        search_terms.append(stage)
        # From recent research
        for brief in state.get("research_briefs", [])[-2:]:
            search_terms.extend(brief.split()[:10])
        # From validation failures
        if state.get("last_validation") and not state["last_validation"]["valid"]:
            for err in state["last_validation"]["errors"]:
                search_terms.extend(err.split()[:5])
        
        # Dedupe and clean
        search_terms = list(set([t.lower().strip(",.()\"") for t in search_terms if len(t) > 3]))[:20]
        
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

    def run_culler(self, keywords):
        try:
            cmd = ["python", "tools/context_culler.py"] + keywords
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)
            return result.stdout if result.returncode == 0 else "Culler failed."
        except Exception as e:
            return f"Culler error: {str(e)}"
        
    def _get_research_context(self, state):
        briefs = state.get("research_briefs", [])
        if not briefs:
            return "No research briefs available yet."
            
        research_content = ""
        for brief_path in briefs[-3:]: # Include last 3 briefs
            if os.path.exists(brief_path):
                try:
                    with open(brief_path, 'r', encoding='utf-8') as f:
                        # Get a compact version: Status, Query, and Findings
                        lines = f.readlines()
                        content = "".join(lines[:30]) # First 30 lines (usually enough for overview + some findings)
                        research_content += f"### {os.path.basename(brief_path)}\n{content}\n\n"
                except Exception as e:
                    research_content += f"### {os.path.basename(brief_path)}\nError reading brief: {str(e)}\n\n"
        return research_content

    def generate_slug(self, text):
        import re
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9 ]', '', slug)
        slug = slug.replace(' ', '_')
        return slug[:48]
