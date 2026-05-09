import os
import json

class TestRunner:
    def __init__(self, command_runner):
        self.command_runner = command_runner

    def run_typecheck(self):
        print("Running typecheck...")
        res = self.command_runner.run("typecheck")
        return {
            "ran": True,
            "success": res.get("success", False),
            "stdout": res.get("stdout", ""),
            "stderr": res.get("stderr", "")
        }

    def run_tests(self, target=None):
        print(f"Running tests {f'for {target}' if target else ''}...")
        if target:
            res = self.command_runner.run("test_target", args=[target])
        else:
            res = self.command_runner.run("test")
            
        return {
            "ran": True,
            "success": res.get("success", False),
            "stdout": res.get("stdout", ""),
            "stderr": res.get("stderr", "")
        }

    def run_bloat(self):
        print("Running bloat check...")
        res = self.command_runner.run("find_bloat", args=["--json"])
        violations = []
        if res.get("stdout"):
            try:
                violations = json.loads(res["stdout"])
            except:
                pass
        return {
            "ran": True,
            "success": res.get("success", False),
            "violations": violations
        }

    def run_full_suite(self):
        return {
            "typecheck": self.run_typecheck(),
            "tests": self.run_tests(),
            "bloat": self.run_bloat()
        }
