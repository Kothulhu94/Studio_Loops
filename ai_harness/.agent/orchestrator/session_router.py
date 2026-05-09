import json
import os
from datetime import datetime


class SessionRouter:
    SESSION_KINDS = {"feature", "bug", "asset", "design", "research", "implementation"}

    KIND_ROUTES = {
        "feature": "concept_producer",
        "design": "concept_producer",
        "research": "researcher",
        "asset": "asset_creator",
        "bug": "bug_hunter",
        "implementation": "developer",
    }

    KIND_ALLOWED_ROLES = {
        "feature": ["concept_producer", "researcher", "designer", "asset_creator", "developer", "qa_tester", "bug_hunter", "debug_dev"],
        "design": ["concept_producer", "researcher", "designer", "asset_creator", "developer", "qa_tester"],
        "research": ["researcher", "designer", "developer"],
        "asset": ["asset_creator", "designer", "developer", "qa_tester"],
        "bug": ["bug_hunter", "debug_dev", "qa_tester"],
        "implementation": ["developer", "qa_tester", "bug_hunter", "debug_dev"],
    }

    KIND_COMPLETION_CRITERIA = {
        "feature": ["Feature reaches QA PASS or handover_complete."],
        "design": ["Design spec exists and downstream implementation handoff is clear."],
        "research": ["Research-backed technical audit and implementation blueprint are complete."],
        "asset": ["Asset specs or generated assets and integration plan are complete."],
        "bug": ["Root cause, fix, and regression verification are complete."],
        "implementation": ["Code changes, tests, and verification report are complete."],
    }

    def __init__(self, workspace_root, sessions_dir=".agent/state/sessions"):
        self.workspace_root = workspace_root
        self.sessions_dir = os.path.join(workspace_root, sessions_dir)

    def infer_kind(self, request_text):
        request = (request_text or "").lower()
        if any(word in request for word in ["bug", "fix", "broken", "error", "failure", "crash", "regression"]):
            return "bug"
        if any(word in request for word in ["asset", "sprite", "icon", "tileset", "sound", "animation"]):
            return "asset"
        if any(word in request for word in ["research", "how to", "architecture", "compare", "investigate"]):
            return "research"
        if any(word in request for word in ["design", "ui", "look", "aesthetic", "layout", "ux"]):
            return "design"
        if any(word in request for word in ["implement", "build", "code", "add", "create"]):
            return "implementation"
        return "feature"

    def route_initial_stage(self, request_text, kind=None):
        resolved_kind = kind or self.infer_kind(request_text)
        return self.KIND_ROUTES.get(resolved_kind, "concept_producer")

    def create_session(self, title, slug, kind=None, start_stage=None):
        resolved_kind = kind or self.infer_kind(title)
        if resolved_kind not in self.SESSION_KINDS:
            resolved_kind = "feature"

        now = datetime.now().isoformat()
        session_id = self._make_session_id(slug, now)
        initial_stage = start_stage or self.route_initial_stage(title, resolved_kind)

        return {
            "session_id": session_id,
            "kind": resolved_kind,
            "title": title,
            "slug": slug,
            "feature": title,
            "feature_slug": slug,
            "active": True,
            "status": "running",
            "current_stage": initial_stage,
            "allowed_roles": self.KIND_ALLOWED_ROLES.get(resolved_kind, self.KIND_ALLOWED_ROLES["feature"]),
            "workspace_roots": ["src", "tests", "tools", "data", "docs", ".agent/Loop_Flow"],
            "artifact_root": ".agent/Loop_Flow",
            "memory_root": f".agent/Loop_Flow/context_packs/{slug}",
            "completion_criteria": self.KIND_COMPLETION_CRITERIA.get(resolved_kind, []),
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
            "created_at": now,
            "updated_at": now,
            "archived_at": None,
        }

    def list_sessions(self):
        if not os.path.exists(self.sessions_dir):
            return []
        sessions = []
        for name in sorted(os.listdir(self.sessions_dir)):
            if not name.endswith(".json"):
                continue
            try:
                with open(os.path.join(self.sessions_dir, name), "r", encoding="utf-8") as handle:
                    sessions.append(json.load(handle))
            except Exception:
                continue
        return sessions

    def session_path(self, session_id):
        return os.path.join(self.sessions_dir, f"{session_id}.json")

    def _make_session_id(self, slug, timestamp):
        compact_time = timestamp.replace("-", "").replace(":", "").replace(".", "").replace("T", "_")
        return f"{slug}_{compact_time}"
