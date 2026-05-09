import os
import json

class ArtifactStore:
    def __init__(self, artifact_dir=".agent/Loop_Flow/"):
        self.artifact_dir = artifact_dir

    def save_artifact(self, name, content, metadata=None):
        os.makedirs(self.artifact_dir, exist_ok=True)
        path = os.path.join(self.artifact_dir, name)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        if metadata:
            meta_path = path + ".meta.json"
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
        
        return path

    def load_artifact(self, name):
        path = os.path.join(self.artifact_dir, name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def list_artifacts(self):
        if not os.path.exists(self.artifact_dir):
            return []
        return [f for f in os.listdir(self.artifact_dir) if not f.endswith(".meta.json")]
