import os
import re
import json

class SourceIndexer:
    def __init__(self, workspace_root):
        self.workspace_root = workspace_root
        self.ignore_dirs = {".git", "node_modules", "dist", "build", ".agent/logs", ".agent/state", ".agent/Loop_Flow/context_packs"}
        self.index_path = os.path.join(self.workspace_root, ".agent/Loop_Flow/source_index.json")

    def index_project(self):
        index = []
        for root, dirs, files in os.walk(self.workspace_root):
            # Filter dirs in-place
            new_dirs = []
            for d in dirs:
                rel_dir = os.path.relpath(os.path.join(root, d), self.workspace_root).replace("\\", "/")
                if rel_dir in self.ignore_dirs:
                    continue
                # Skip other hidden dirs unless it's .agent
                if d.startswith(".") and d != ".agent":
                    continue
                new_dirs.append(d)
            dirs[:] = new_dirs
            
            for file in files:
                if file.endswith(('.py', '.ts', '.js', '.css', '.html', '.md')):
                    rel_path = os.path.relpath(os.path.join(root, file), self.workspace_root).replace("\\", "/")
                    file_info = self._analyze_file(rel_path)
                    index.append(file_info)
        
        # Save index
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
            
        return index

    def _analyze_file(self, rel_path):
        full_path = os.path.join(self.workspace_root, rel_path)
        info = {
            "path": rel_path,
            "line_count": 0,
            "symbols": [],
            "imports": []
        }
        
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                info["line_count"] = len(lines)
                content = "".join(lines)
                
                # Simple regex for symbols
                if rel_path.endswith('.py'):
                    info["symbols"] = re.findall(r'^(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE)
                    info["imports"] = re.findall(r'^(?:from|import)\s+([a-zA-Z0-9_.]+)', content, re.MULTILINE)
                elif rel_path.endswith(('.ts', '.js')):
                    info["symbols"] = re.findall(r'(?:class|function|interface|export\s+(?:const|let|var|class|function|interface))\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                    info["imports"] = re.findall(r'import\s+.*\s+from\s+[\'"](.*)[\'"]', content)
        except:
            pass
            
        return info

    def generate_context_summary(self, limit=50):
        if not os.path.exists(self.index_path):
            self.index_project()
            
        with open(self.index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
            
        summary = "Relevant Source Files:\n"
        for item in index[:limit]:
            summary += f"- {item['path']} ({item['line_count']} lines)"
            if item["symbols"]:
                summary += f" | Symbols: {', '.join(item['symbols'][:5])}"
            summary += "\n"
        return summary
