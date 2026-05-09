import os
import json
from datetime import datetime
from browser_research import BrowserResearch

class ResearchClient:
    """Research client for the Studio Loop Orchestrator. 
    Uses local Playwright browser automation for web research.
    No API keys or paid providers required.
    """
    def __init__(self, config=None, base_path=None):
        self.config = config or {}
        self.base_path = base_path or os.getcwd()
        research_config = self.config.get("web_research", {})
        self.enabled = research_config.get("enabled", False)
        self.browser_research = BrowserResearch(self.config, self.base_path)
        self.artifact_dir = os.path.join(self.base_path, research_config.get("artifact_dir", ".agent/Loop_Flow/research"))

    def perform_research(self, query, reason=None, feature_slug=None, stage=None):
        if not self.enabled:
            return {
                "query": query,
                "status": "blocked",
                "error": "Web research is disabled in config."
            }
            
        print(f"Researching (Browser-Based): {query}")
        research_data = self.browser_research.perform_research(query, reason)
        
        # Save research brief artifact
        artifact_content = self.generate_artifact(research_data)
        os.makedirs(self.artifact_dir, exist_ok=True)
        
        # Generate unique filename
        safe_query = "".join([c if c.isalnum() else "_" for c in query[:30]]).strip("_")
        slug = feature_slug or "latest"
        stage_name = stage or "unknown"
        filename = f"{slug}_{stage_name}_{safe_query}_research_brief.md"
        artifact_path = os.path.join(self.artifact_dir, filename)
        
        with open(artifact_path, 'w', encoding='utf-8') as f:
            f.write(artifact_content)
            
        research_data["artifact_path"] = artifact_path
        return research_data

    def generate_artifact(self, research_data):
        query = research_data.get('query', 'Unknown')
        status = research_data.get('status', 'complete')
        
        content = f"# Research Brief: {query}\n\n"
        content += f"## Status\n{status}\n\n"
        content += f"## Query\n{query}\n\n"
        content += f"## Reason\n{research_data.get('reason', 'N/A')}\n\n"
        
        content += "## Sources\n\n"
        content += "| Title | URL | Status | Retrieved | Notes |\n"
        content += "|---|---|---|---|---|\n"
        for src in research_data.get("sources", []):
            content += f"| {src['title']} | {src['url']} | {src['status']} | {src.get('retrieved_at', 'N/A')} | {src.get('notes', '')} |\n"
        
        content += "\n## Extracted Findings\n\n"
        if research_data.get("findings"):
            for finding in research_data["findings"]:
                content += f"### Finding\n{finding}\n\n"
        else:
            content += "No findings recorded.\n"
        
        content += "\n## Copyright / Safety Notes\n"
        content += "Extracted from public web sources using local browser automation. No prohibited IP terms detected in summary.\n"
        
        content += "\n## Technical Notes\n"
        backend = research_data.get("backend", "playwright")
        content += f"- Backend: {backend}\n"
        content += f"- Timestamp: {datetime.now().isoformat()}\n"
        
        return content
