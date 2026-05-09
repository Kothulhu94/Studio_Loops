import subprocess
import os
import json
import re
from datetime import datetime

class CommandRunner:
    SHELL_METACHRACTERS = r'[;&|><$\(\)\x60]'

    def __init__(self, workspace_root, allowlist_path, logs_dir=".agent/logs/commands/"):
        self.workspace_root = os.path.abspath(workspace_root)
        with open(os.path.join(self.workspace_root, allowlist_path), 'r') as f:
            self.allowlist = json.load(f)
        self.logs_dir = os.path.join(self.workspace_root, logs_dir)

    def _resolve_command_parts(self, cmd_spec):
        drive = os.path.splitdrive(self.workspace_root)[0] or "C:"
        
        if isinstance(cmd_spec, list):
            resolved = []
            for part in cmd_spec:
                resolved.append(part.replace("{drive}", drive))
            return resolved
        else:
            # Legacy string support
            cmd_str = cmd_spec.replace("{drive}", drive)
            if cmd_str.startswith("\\") and not cmd_str.startswith("\\\\"):
                return [drive + cmd_str]
            return cmd_str.split()

    def run(self, command_name, args=None, timeout=None):
        cmd_entry = next((c for c in self.allowlist["allowed_commands"] if c["name"] == command_name), None)
        if not cmd_entry:
            return {"success": False, "error": f"Command '{command_name}' is not in the allowlist."}

        # 1. Determine timeout
        exec_timeout = timeout or cmd_entry.get("timeout", 60)

        # 2. Check if args are permitted
        if args and not cmd_entry.get("allow_args", False):
            return {"success": False, "error": f"Command '{command_name}' does not permit arguments."}

        full_cmd_list = self._resolve_command_parts(cmd_entry["command"])
        
        # 3. Validate and append args
        if args:
            if not isinstance(args, list):
                args = [str(args)]
            
            arg_pattern = cmd_entry.get("arg_pattern")
            for arg in args:
                # Regex validation for args
                if arg_pattern and not re.match(arg_pattern, arg):
                    return {"success": False, "error": f"Argument '{arg}' does not match permitted pattern '{arg_pattern}'."}
                
                # Reject shell metacharacters
                if re.search(self.SHELL_METACHRACTERS, arg):
                    return {"success": False, "error": f"Argument '{arg}' contains forbidden shell metacharacters."}
                full_cmd_list.append(arg)

        # 4. Check for blocked patterns in final list
        full_cmd_str = " ".join(full_cmd_list)
        for pattern in self.allowlist.get("blocked_patterns", []):
            if pattern in full_cmd_str:
                return {"success": False, "error": f"Blocked pattern '{pattern}' detected in full command."}

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Use shell=False for list-based commands (safer)
            # Only use shell=True if explicitly required (e.g., .bat files)
            use_shell = cmd_entry.get("requires_shell", False)
            
            result = subprocess.run(
                full_cmd_list, 
                shell=use_shell, 
                cwd=self.workspace_root,
                capture_output=True, 
                text=True,
                timeout=exec_timeout
            )
            
            output = {
                "name": command_name,
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": full_cmd_str
            }
            
            self._log_command(command_name, output, timestamp)
            return output
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {exec_timeout} seconds."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _log_command(self, name, result, timestamp):
        os.makedirs(self.logs_dir, exist_ok=True)
        log_path = os.path.join(self.logs_dir, f"{name}_{timestamp}.json")
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
