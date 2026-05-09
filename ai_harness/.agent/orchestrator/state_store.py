import json
import os
from datetime import datetime
from session_router import SessionRouter

class StateStore:
    def __init__(self, state_path):
        self.state_path = state_path
        self.workspace_root = os.path.abspath(os.path.join(os.path.dirname(state_path), "..", ".."))
        self.session_router = SessionRouter(self.workspace_root)

    def load_state(self):
        if not os.path.exists(self.state_path):
            return self.reset_state()
        with open(self.state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        active_session_id = state.get("active_session_id")
        if active_session_id:
            session_path = self.session_router.session_path(active_session_id)
            if os.path.exists(session_path):
                with open(session_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return state

    def save_state(self, state):
        state["updated_at"] = datetime.now().isoformat()
        if state.get("session_id"):
            os.makedirs(self.session_router.sessions_dir, exist_ok=True)
            with open(self.session_router.session_path(state["session_id"]), 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            pointer = self._pointer_state(state["session_id"], state)
            os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(pointer, f, indent=2)
            return
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

    def reset_state(self):
        state = {
            "active_session_id": None,
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

    def start_feature(self, feature_text, slug, start_stage, kind=None):
        state = self.session_router.create_session(feature_text, slug, kind=kind, start_stage=start_stage)
        self.save_state(state)
        return state

    def list_sessions(self):
        return self.session_router.list_sessions()

    def get_session(self, session_id):
        session_path = self.session_router.session_path(session_id)
        if not os.path.exists(session_path):
            raise FileNotFoundError(f"Session not found: {session_id}")
        with open(session_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def resume_session(self, session_id):
        state = self.get_session(session_id)
        if state.get("status") == "archived":
            state["status"] = "running" if state.get("active") else "idle"
            state["archived_at"] = None
        self.save_state(state)
        return state

    def archive_session(self, session_id):
        session_path = self.session_router.session_path(session_id)
        if not os.path.exists(session_path):
            raise FileNotFoundError(f"Session not found: {session_id}")
        with open(session_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        state["status"] = "archived"
        state["active"] = False
        state["archived_at"] = datetime.now().isoformat()
        self.save_state(state)
        pointer = self._pointer_state(None, state)
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(pointer, f, indent=2)
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
        previous_stage = state.get("current_stage")
        if stage_name == "handover_complete":
            state["current_stage"] = stage_name
            state["status"] = "complete"
            state["active"] = False
            self._record_transition(state, previous_stage, stage_name)
            self.save_state(state)
            return
        state["current_stage"] = stage_name
        state["status"] = "running"
        self._record_transition(state, previous_stage, stage_name)
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

    def record_skills_used(self, stage_name, skills):
        state = self.load_state()
        if "skills_used" not in state:
            state["skills_used"] = {}
        state["skills_used"][stage_name] = [
            {
                "id": skill["id"],
                "version": skill["version"],
                "trust_level": skill["trust_level"],
                "manifest": skill.get("_manifest_path"),
            }
            for skill in skills
        ]
        self.save_state(state)

    def _record_transition(self, state, from_stage, to_stage):
        if from_stage == to_stage:
            return
        if "transition_history" not in state:
            state["transition_history"] = []
        state["transition_history"].append({
            "from": from_stage,
            "to": to_stage,
            "timestamp": datetime.now().isoformat()
        })

    def _pointer_state(self, active_session_id, session_state):
        return {
            "active_session_id": active_session_id,
            "active": bool(active_session_id and session_state.get("active")),
            "status": session_state.get("status", "idle"),
            "feature": session_state.get("feature"),
            "feature_slug": session_state.get("feature_slug"),
            "current_stage": session_state.get("current_stage"),
            "updated_at": datetime.now().isoformat(),
        }
