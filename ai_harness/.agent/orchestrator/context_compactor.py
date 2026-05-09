import os
import json
from datetime import datetime

class ContextCompactor:
    def __init__(self, workspace_root):
        self.workspace_root = workspace_root
        self.memory_dir = os.path.join(self.workspace_root, ".agent/Loop_Flow/context_packs")

    def compact(self, feature_slug, stage, state):
        if not state or not feature_slug:
            return None
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # 1. Generate Stage Summary
        summary_content = self._generate_stage_summary(stage, state)
        summary_path = os.path.join(self.memory_dir, f"{feature_slug}_stage_summary.md")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
            
        # 2. Update Decision Memory
        self._update_decision_memory(feature_slug, state)
        
        # 3. Compact Last Errors
        self._compact_errors(feature_slug, state)
        
        return summary_path

    def _generate_stage_summary(self, stage, state):
        last_actions = state.get("last_actions", {})
        summary = f"# Stage Summary: {stage}\n\n"
        summary += f"Status: {last_actions.get('status', 'unknown')}\n"
        summary += f"Summary: {last_actions.get('summary', 'N/A')}\n\n"
        
        summary += "## Artifacts Produced\n"
        for art in state.get("artifacts", {}):
            summary += f"- {art}\n"
            
        return summary

    def _update_decision_memory(self, feature_slug, state):
        path = os.path.join(self.memory_dir, f"{feature_slug}_decision_memory.md")
        last_actions = state.get("last_actions", {})
        
        content = f"# Decision Memory: {feature_slug}\n\n"
        
        content += "## Stable Decisions\n"
        content += f"- {last_actions.get('summary', 'Initial implementation started.')}\n\n"
        
        content += "## Constraints\n"
        content += "- Adhere to Studio Loop safety guidelines.\n"
        content += "- Use Playwright for research.\n\n"
        
        content += "## Files Changed\n"
        for write in state.get("last_results", {}).get("writes", []):
            if write["success"]:
                content += f"- {write['path']}\n"
        for patch in state.get("last_results", {}).get("patches", []):
            if patch["success"]:
                content += f"- {patch['path']}\n"
        content += "\n"
        
        content += "## Research Used\n"
        for res in state.get("research_results", []):
            content += f"- {res['query']} ({res['status']})\n"
        content += "\n"
        
        content += "## Validation Failures\n"
        for fail in state.get("failures", []):
            content += f"- {fail['stage']}: {fail['reason']}\n"
        content += "\n"
        
        content += "## Next Stage Notes\n"
        content += "- Ensure all tests pass before handover.\n"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _compact_errors(self, feature_slug, state):
        path = os.path.join(self.memory_dir, f"{feature_slug}_last_errors.md")
        failures = state.get("failures", [])
        if not failures:
            return
            
        content = "# Last Errors\n\n"
        for fail in failures[-5:]: # Keep last 5
            content += f"### {fail['stage']} ({fail['timestamp']})\n"
            content += f"{fail['reason']}\n\n"
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
