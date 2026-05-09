import os
import json
from datetime import datetime

class OrchestratorHooks:
    def __init__(self, workspace_root, logs_dir=".agent/logs/hooks/"):
        self.workspace_root = workspace_root
        self.logs_dir = os.path.join(self.workspace_root, logs_dir)
        self.callbacks = {}
        
    def register_callback(self, hook_name, callback):
        if hook_name not in self.callbacks:
            self.callbacks[hook_name] = []
        self.callbacks[hook_name].append(callback)

    def trigger(self, hook_name, context=None):
        timestamp = datetime.now().isoformat()
        event = {
            "hook": hook_name,
            "timestamp": timestamp,
            "context_keys": list(context.keys()) if context else []
        }
        
        # Log to file
        os.makedirs(self.logs_dir, exist_ok=True)
        log_file = os.path.join(self.logs_dir, "hooks_history.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {hook_name} | {json.dumps(event['context_keys'])}\n")
            
        # Run callbacks
        if hook_name in self.callbacks:
            for cb in self.callbacks[hook_name]:
                try:
                    cb(context)
                except Exception as e:
                    print(f"Error in hook callback {hook_name}: {e}")

