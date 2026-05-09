import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

class PatchApplier:
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
            "package-lock.json", "pnpm-lock.yaml", "yarn.lock"
        ]

    def apply(self, stage, path, diff_content):
        # 1. Validate stage permissions and safety
        if os.path.isabs(path) or ".." in path:
            return False, f"Invalid patch path: {path}. Absolute paths and parent traversal are forbidden."

        normalized_path = os.path.normpath(path).replace("\\", "/")
        
        # Check stage-specific permissions
        allowed_roots = self.STAGE_PERMISSIONS.get(stage, [])
        is_allowed = False
        for root in allowed_roots:
            root = root.rstrip("/")
            if normalized_path == root or normalized_path.startswith(root + "/"):
                is_allowed = True
                break
        
        if not is_allowed:
            return False, f"Unauthorized path for stage '{stage}': {path}"

        # Check blocked targets
        for blocked in self.blocked_targets:
            if blocked in normalized_path:
                return False, f"Patch targeting blocked file '{blocked}' is forbidden."

        full_path = os.path.join(self.workspace_root, path)
        if not os.path.exists(full_path):
            return False, f"Target file for patch does not exist: {path}"

        # 2. Create a temp diff file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".diff", mode="w", encoding="utf-8") as diff_file:
            diff_file.write(diff_content)
            diff_file_path = diff_file.name

        try:
            # 3. Dry-run first with 'git apply --check'
            check_result = subprocess.run(
                ["git", "apply", "--check", "--whitespace=fix", diff_file_path],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            
            if check_result.returncode != 0:
                self._log_patch(path, diff_content, success=False, error=f"Check failed: {check_result.stderr}")
                return False, f"Patch check failed: {check_result.stderr}"

            # 4. Apply for real
            apply_result = subprocess.run(
                ["git", "apply", "--whitespace=fix", diff_file_path],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            
            if apply_result.returncode == 0:
                self._log_patch(path, diff_content, success=True)
                return True, None
            else:
                self._log_patch(path, diff_content, success=False, error=apply_result.stderr)
                return False, f"Patch apply failed: {apply_result.stderr}"

        except Exception as e:
            return False, f"Patch execution error: {str(e)}"
        finally:
            if os.path.exists(diff_file_path): 
                os.remove(diff_file_path)

    def _log_patch(self, rel_path, diff, success, error=None):
        os.makedirs(self.logs_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "SUCCESS" if success else "FAILED"
        log_name = f"patch_{timestamp}_{status}.diff"
        
        with open(os.path.join(self.logs_dir, log_name), "w", encoding="utf-8") as f:
            f.write(f"Target: {rel_path}\n")
            if error:
                f.write(f"Error: {error}\n")
            f.write("-" * 40 + "\n")
            f.write(diff)
