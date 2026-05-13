import json
import os
from copy import deepcopy
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
        
        try:
            with open(self.state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading pointer state: {e}. Resetting.")
            return self.reset_state()

        active_session_id = state.get("active_session_id")
        if active_session_id:
            session_path = self.session_router.session_path(active_session_id)
            if os.path.exists(session_path):
                try:
                    with open(session_path, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                        # Ensure the session data is actually for this session_id
                        if session_data.get("session_id") == active_session_id:
                            return session_data
                        else:
                            print(f"Session data mismatch for {active_session_id}. Falling back to pointer.")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading session {active_session_id}: {e}. Falling back to pointer.")
            else:
                print(f"Warning: Active session file missing: {session_path}. Feature context will be limited.")
                if state.get("active"):
                    return self._recover_missing_session(state, active_session_id)
        
        return self._ensure_state_shape(state)

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
        
        # New: Record detailed stage result components (stripped of large blobs)
        if "actions" in result:
            actions = json.loads(json.dumps(result["actions"])) # Deep copy
            if "writes" in actions:
                for w in actions["writes"]:
                    if "content" in w:
                        w["content"] = "[content written to disk - omitted from state to save context]"
            if "patches" in actions:
                for p in actions["patches"]:
                    if "diff" in p:
                        p["diff"] = "[stripped for brevity]"
            state["last_actions"] = actions
        
        if "results" in result:
            results = json.loads(json.dumps(result["results"])) # Deep copy
            if "writes" in results:
                for w in results["writes"]:
                    if "content" in w:
                        w["content"] = "[stripped for brevity]"
            if "patches" in results:
                for p in results["patches"]:
                    if "diff" in p:
                        p["diff"] = "[diff applied to disk - omitted from state to save context]"
            state["last_results"] = results
            
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
        state.setdefault("context_packs", {})
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

    def _default_state(self):
        return {
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
            "transition_history": [],
            "skills_used": {},
            "last_model_response_path": None,
            "last_actions": None,
            "last_results": None,
            "last_validation": None,
            "last_transition": None,
            "capabilities": {},
            "created_at": None,
            "updated_at": None,
            "archived_at": None,
        }

    def _ensure_state_shape(self, state):
        if not isinstance(state, dict):
            return self.reset_state()
        defaults = self._default_state()
        for key, value in defaults.items():
            state.setdefault(key, deepcopy(value))

        active_session_id = state.get("active_session_id")
        if active_session_id and not state.get("session_id"):
            state["session_id"] = active_session_id
        if state.get("feature") and not state.get("title"):
            state["title"] = state["feature"]
        if state.get("feature_slug") and not state.get("slug"):
            state["slug"] = state["feature_slug"]

        kind = state.get("kind")
        if not kind and state.get("feature"):
            kind = self.session_router.infer_kind(state.get("feature"))
            state["kind"] = kind
        if not state.get("stack_profile"):
            state["stack_profile"] = "harness_internal" if kind == "harness_upgrade" else "game_source"

        if kind:
            if not state.get("allowed_roles"):
                state["allowed_roles"] = self.session_router.KIND_ALLOWED_ROLES.get(
                    kind,
                    self.session_router.KIND_ALLOWED_ROLES["feature"],
                )
            if not state.get("completion_criteria"):
                state["completion_criteria"] = self.session_router.KIND_COMPLETION_CRITERIA.get(kind, [])
        return state

    def _recover_missing_session(self, pointer_state, active_session_id):
        feature = pointer_state.get("feature") or "Recovered Studio Loop session"
        slug = pointer_state.get("feature_slug") or str(active_session_id).rsplit("_", 1)[0] or "recovered_session"
        kind = pointer_state.get("kind") or self.session_router.infer_kind(feature)
        stage = pointer_state.get("current_stage") or self.session_router.route_initial_stage(feature, kind)
        recovered = self.session_router.create_session(feature, slug, kind=kind, start_stage=stage)
        recovered["session_id"] = active_session_id
        recovered["active"] = bool(pointer_state.get("active", True))
        recovered["status"] = pointer_state.get("status", "running")
        recovered["current_stage"] = stage
        recovered["created_at"] = pointer_state.get("created_at") or pointer_state.get("updated_at") or recovered["created_at"]

        for key, value in pointer_state.items():
            if key in {"active_session_id", "session_id"}:
                continue
            if value is not None:
                recovered[key] = value

        recovered = self._ensure_state_shape(recovered)
        print(f"Recovered missing active session metadata into: {self.session_router.session_path(active_session_id)}")
        self.save_state(recovered)
        return recovered
