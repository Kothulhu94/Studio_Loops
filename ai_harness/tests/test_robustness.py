import unittest
import os
import shutil
import json
import subprocess
import time
from datetime import datetime

class TestRobustness(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.original_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = os.path.join(self.temp_dir_obj.name, "workspace")
        shutil.copytree(
            self.original_base_dir,
            self.base_dir,
            ignore=shutil.ignore_patterns("node_modules", ".git", ".agent/logs/*", "__pycache__"),
        )
        self.orchestrator_path = os.path.join(self.base_dir, ".agent/orchestrator/studio_loop.py")

    def tearDown(self):
        self.temp_dir_obj.cleanup()
        
    def test_reset_cleans_artifacts(self):
        # Create dummy artifacts
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow/research"), exist_ok=True)
        dummy_file = os.path.join(self.base_dir, ".agent/Loop_Flow/research/dummy.md")
        with open(dummy_file, 'w') as f:
            f.write("dummy")
        session_dir = os.path.join(self.base_dir, ".agent/state/sessions")
        os.makedirs(session_dir, exist_ok=True)
        old_session = os.path.join(session_dir, "old_active.json")
        with open(old_session, "w", encoding="utf-8") as f:
            json.dump({"active": True, "status": "running"}, f)
        lock_path = os.path.join(self.base_dir, ".agent/state/studio_loop.lock")
        with open(lock_path, "w", encoding="utf-8") as f:
            json.dump({"pid": 123456}, f)
            
        # Run reset
        subprocess.run(["python", self.orchestrator_path, "reset"], cwd=self.base_dir, check=True)
        
        # Verify cleaned
        self.assertFalse(os.path.exists(dummy_file))
        self.assertFalse(os.path.exists(old_session))
        self.assertFalse(os.path.exists(lock_path))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, ".agent/Loop_Flow/research/.gitkeep")))

    def test_process_lock(self):
        # Actually, let's just manually create a lock and try to run status (status shouldn't be blocked)
        lock_path = os.path.join(self.base_dir, ".agent/state/studio_loop.lock")
        os.makedirs(os.path.dirname(lock_path), exist_ok=True)
        with open(lock_path, 'w') as f:
            json.dump({"pid": 99999, "timestamp": datetime.now().isoformat()}, f)
            
        # Try to run 'run' which should fail if PID 99999 was alive (it's not, so it should recover)
        # To test failure, we need a REAL live PID.
        import psutil
        my_pid = os.getpid()
        with open(lock_path, 'w') as f:
            json.dump({"pid": my_pid, "timestamp": datetime.now().isoformat()}, f)
            
        # Now run a command that acquires lock
        result = subprocess.run(["python", self.orchestrator_path, "run", "test"], cwd=self.base_dir, capture_output=True, text=True)
        self.assertIn("Another orchestrator", result.stdout)
        self.assertNotEqual(result.returncode, 0)
        
        # Cleanup
        os.remove(lock_path)

if __name__ == "__main__":
    unittest.main()
