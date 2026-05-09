import json
import os
from datetime import datetime

class StateStore:
    def __init__(self, state_path):
        self.state_path = state_path

    def load_state(self):
        if not os.path.exists(self.state_path):
            return self.reset_state()
        with open(self.state_path, 'r') as f:
            return json.load(f)

    def save_state(self, state):
        state["updated_at"] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=2)

    def reset_state(self):
        state = {
            "active": False,
            "feature": None,
            "feature_slug": None,
            "status": "idle",
            "current_stage": None,
            "completed_stages": [],
            "stage_attempts": {},
            "artifacts": {},
            "context_packs": {},
            "research_briefs": [],
            "research_results": [],
            "research_request_history": [],
            "research_duplicate_warnings": {},
            "writes": [],
            "patches": [],
            "commands": [],
            "tests": [],
            "validations": [],
            "failures": [],
            "blockers": [],
            "last_model_response_path": None,
            "last_actions": None,
            "last_results": None,
            "last_validation": None,
            "last_transition": None,
            "capabilities": {},
            "created_at": None,
            "updated_at": None
        }
        self.save_state(state)
        return state

    def start_feature(self, feature_text, slug, start_stage):
        state = self.reset_state()
        state["active"] = True
        state["feature"] = feature_text
        state["feature_slug"] = slug
        state["status"] = "running"
        state["current_stage"] = start_stage
        state["created_at"] = datetime.now().isoformat()
        self.save_state(state)
        return state

    def complete_stage(self, stage_name, result):
        state = self.load_state()
        if stage_name not in state["completed_stages"]:
            state["completed_stages"].append(stage_name)
        
        # New: Record detailed stage result components
        if "actions" in result:
            state["last_actions"] = result["actions"]
        
        if "results" in result:
            state["last_results"] = result["results"]
            
        # Record artifacts from result
        for art in result.get("artifacts_written", []):
            state["artifacts"][art] = art 
            
        # Also record writes as artifacts if they are in the Loop_Flow
        if "results" in result and "writes" in result["results"]:
            for w in result["results"]["writes"]:
                # Normalize path for robust matching across OS/separators
                clean_path = os.path.normpath(w["path"]).replace("\\", "/")
                if w.get("success") and ".agent/Loop_Flow" in clean_path:
                    basename = os.path.basename(clean_path)
                    state["artifacts"][basename] = clean_path
            
        self.save_state(state)

    def fail_stage(self, stage_name, reason):
        state = self.load_state()
        state["failures"].append({
            "stage": stage_name,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        state["status"] = "failed"
        self.save_state(state)

    def set_current_stage(self, stage_name):
        state = self.load_state()
        if stage_name == "handover_complete":
            state["current_stage"] = stage_name
            state["status"] = "complete"
            state["active"] = False
            self.save_state(state)
            return
        state["current_stage"] = stage_name
        state["status"] = "running"
        self.save_state(state)

    def record_artifact(self, key, path):
        state = self.load_state()
        state["artifacts"][key] = path
        self.save_state(state)

    def record_context_pack(self, stage_name, path):
        state = self.load_state()
        state["context_packs"][stage_name] = path
        self.save_state(state)

    def update_capabilities(self, capabilities):
        state = self.load_state()
        state["capabilities"] = capabilities
        self.save_state(state)
