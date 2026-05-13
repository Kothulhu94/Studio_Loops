import os
import sys
import unittest
import json
import tempfile
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from state_store import StateStore

class TestStateCompaction(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.test_dir, "state.json")
        self.store = StateStore(self.state_path)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_complete_stage_strips_content(self):
        result = {
            "actions": {
                "writes": [{"path": "test.txt", "content": "A" * 10000}]
            },
            "results": {
                "writes": [{"path": "test.txt", "content": "A" * 10000, "success": True}]
            }
        }
        
        self.store.complete_stage("developer", result)
        state = self.store.load_state()
        
        self.assertEqual(state["last_actions"]["writes"][0]["content"], "[content written to disk - omitted from state to save context]")
        self.assertEqual(state["last_results"]["writes"][0]["content"], "[stripped for brevity]")

if __name__ == "__main__":
    unittest.main()
