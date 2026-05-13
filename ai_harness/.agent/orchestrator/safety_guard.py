import os
import json
import re

class SafetyGuard:
    def __init__(self, workspace_root):
        self.workspace_root = workspace_root
        self.stage_write_policy = {}
        self.session_workspace_roots = []
        self.allowed_roots = [
            "src/", "tests/", "tools/", "data/", "docs/", "public/",
            ".agent/Loop_Flow/", ".agent/logs/", ".agent/state/", 
            ".agent/orchestrator/", ".agent/workflows/", ".agent/skills/"
        ]
        self.blocked_files = [
            "package-lock.json",
            "pnpm-lock.yaml",
            "yarn.lock",
            ".env"
        ]
        self.allowlist_path = os.path.join(workspace_root, ".agent/orchestrator/command_allowlist.json")
        self._allowlist = None

    def set_policy_context(self, stage_write_policy=None, session_workspace_roots=None):
        self.stage_write_policy = stage_write_policy or {}
        self.session_workspace_roots = session_workspace_roots or []

    @property
    def allowlist(self):
        if self._allowlist is None:
            try:
                with open(self.allowlist_path, 'r') as f:
                    self._allowlist = json.load(f)
            except Exception:
                self._allowlist = {"allowed_commands": [], "blocked_patterns": []}
        return self._allowlist

    def is_path_safe(self, path, stage=None):
        # Normalize
        path = path.replace("\\", "/")
        
        # Prevent traversal
        if ".." in path or path.startswith("/"):
            return False

        # Block specific sensitive files
        basename = os.path.basename(path)
        if basename in self.blocked_files:
            return False
            
        # Specific blocks requested
        sensitive_paths = [
            ".agent/orchestrator/config.json",
            "package.json",
            "tsconfig.json"
        ]
        if any(path == sp or path.endswith("/" + sp) for sp in sensitive_paths):
            return False
            
        if basename.startswith("vite.config.") or \
           basename.startswith(".env"):
            return False
            
        # Refined lockfile block
        lock_files = ["package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"]
        if basename in lock_files:
            return False

        # Stage-specific permissions supplied by active skill/session policy.
        permissions = self.stage_write_policy or {
            "concept_producer": [".agent/Loop_Flow", "docs/adr"],
            "researcher": [".agent/Loop_Flow", "docs/adr"],
            "designer": [".agent/Loop_Flow", "public"],
            "asset_creator": [".agent/Loop_Flow", "src/assets", "data/assets", "src/SVG", "public/assets"],
            "developer": ["src", "tests", "tools", "data", "public", ".agent/Loop_Flow", "docs/adr"],
            "qa_tester": [".agent/Loop_Flow", "tests"],
            "bug_hunter": [".agent/Loop_Flow", "tools"],
            "debug_dev": ["src", "tests", "tools", ".agent/Loop_Flow"]
        }
        
        if stage and stage in permissions:
            allowed_for_stage = permissions[stage]
            for root in allowed_for_stage:
                root = root.rstrip("/")
                if path == root or path.startswith(root + "/"):
                    return self._within_session_workspace(path)
            return False

        # Fallback to global allowed roots if no stage provided (for general safety)
        for root in self.allowed_roots:
            root = root.rstrip("/")
            if path == root or path.startswith(root + "/"):
                return True
                
        return False

    def _within_session_workspace(self, path):
        if not self.session_workspace_roots:
            return True
        for root in self.session_workspace_roots:
            root = root.rstrip("/")
            if path == root or path.startswith(root + "/"):
                return True
        return False

    def validate_actions(self, stage, actions):
        """Validates all requested actions for safety."""
        
        # 1. Check writes
        for write in actions.get("writes", []):
            if not self.is_path_safe(write["path"], stage):
                return False, f"Unsafe write path for stage '{stage}': {write['path']}"
            if write.get("mode") not in ["create", "overwrite", "append", None]:
                return False, f"Invalid write mode: {write.get('mode')}"
        
        # 2. Check patches
        for patch in actions.get("patches", []):
            if not self.is_path_safe(patch["path"], stage):
                return False, f"Unsafe patch path for stage '{stage}': {patch['path']}"
            # Block patching dependencies
            if "package.json" in patch["path"] or "node_modules" in patch["path"]:
                return False, f"Patching dependencies is blocked: {patch['path']}"
                
        # 3. Check commands
        allowed_names = [cmd["name"] for cmd in self.allowlist.get("allowed_commands", [])]
        for cmd in actions.get("commands", []):
            if cmd["name"] not in allowed_names:
                return False, f"Command not in allowlist: {cmd['name']}"
            
            # Check for blocked patterns in args
            args_str = str(cmd.get("args", ""))
            for pattern in self.allowlist.get("blocked_patterns", []):
                if pattern in args_str:
                    return False, f"Blocked pattern '{pattern}' detected in command args."

        # 4. Check research requests
        for req in actions.get("research_requests", []):
            if not req.get("query"):
                return False, "Research request missing query."
            if len(req["query"]) < 5:
                return False, "Research query too short."
                
        return True, None
