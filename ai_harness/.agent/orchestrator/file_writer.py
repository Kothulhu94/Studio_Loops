import os
import shutil
from datetime import datetime

class FileWriter:
    STAGE_PERMISSIONS = {
        "concept_producer": [".agent/Loop_Flow", "docs/adr"],
        "researcher": [".agent/Loop_Flow", "docs/adr"],
        "designer": [".agent/Loop_Flow"],
        "asset_creator": [".agent/Loop_Flow", "src/assets", "data/assets", "src/SVG"],
        "developer": ["src", "tests", "tools", "data", ".agent/Loop_Flow", "docs/adr"],
        "qa_tester": [".agent/Loop_Flow", "tests"],
        "bug_hunter": [".agent/Loop_Flow", "tools"],
        "debug_dev": ["src", "tests", "tools", ".agent/Loop_Flow"]
    }

    def __init__(self, workspace_root, logs_dir=".agent/logs/patches/"):
        self.workspace_root = os.path.abspath(workspace_root)
        self.logs_dir = os.path.join(self.workspace_root, logs_dir)
        self.blocked_targets = [
            ".git", "node_modules", "dist", "build", ".env", 
            "package.json", "tsconfig.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"
        ]
        self.stage_write_policy = {}

    def set_policy_context(self, stage_write_policy=None):
        self.stage_write_policy = stage_write_policy or {}

    def write(self, stage, path, content, mode="overwrite"):
        # 1. Normalize and validate path
        full_path, rel_path = self._validate_path(stage, path)
        if not full_path:
            return False, f"Unauthorized or unsafe path for stage '{stage}': {path}"

        # 2. Enforce mode logic
        if mode == "create" and os.path.exists(full_path):
            return False, f"File already exists (mode=create): {path}"
        
        if mode == "overwrite" and os.path.exists(full_path):
            self._save_snapshot(rel_path, full_path)

        # 3. Create parent directories
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # 4. Write file
        try:
            write_mode = "w" if mode in ["overwrite", "create"] else "a"
            with open(full_path, write_mode, encoding="utf-8") as f:
                f.write(content)
            
            self._log_write(rel_path, mode)
            return True, None
        except Exception as e:
            return False, str(e)

    def _validate_path(self, stage, path):
        # Prevent absolute paths or directory traversal
        if os.path.isabs(path) or ".." in path:
            return None, None

        normalized_path = os.path.normpath(path).replace("\\", "/")
        
        # Check stage-specific permissions
        allowed_roots = self.stage_write_policy.get(stage) or self.STAGE_PERMISSIONS.get(stage, [])
        is_allowed = False
        for root in allowed_roots:
            root = root.rstrip("/")
            if normalized_path == root or normalized_path.startswith(root + "/"):
                is_allowed = True
                break
        
        if not is_allowed:
            return None, None

        # Check blocked targets
        for blocked in self.blocked_targets:
            if blocked in normalized_path:
                return None, None

        full_path = os.path.join(self.workspace_root, normalized_path)
        return full_path, normalized_path

    def _save_snapshot(self, rel_path, full_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_dir = os.path.join(self.logs_dir, "snapshots", rel_path)
        os.makedirs(snapshot_dir, exist_ok=True)
        shutil.copy2(full_path, os.path.join(snapshot_dir, f"before_{timestamp}"))

    def _log_write(self, rel_path, mode):
        log_file = os.path.join(self.logs_dir, "write_history.log")
        os.makedirs(self.logs_dir, exist_ok=True)
        timestamp = datetime.now().isoformat()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mode.upper()}: {rel_path}\n")
