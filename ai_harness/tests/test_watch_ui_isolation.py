import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(REPO_ROOT, ".agent/orchestrator"))

from kobold_client import KoboldClient
from research_client import ResearchClient
from safety_guard import SafetyGuard
from session_router import SessionRouter
from source_indexer import SourceIndexer


def load_loop_central_module():
    path = os.path.join(REPO_ROOT, "ui", "loop_central_server.py")
    spec = importlib.util.spec_from_file_location("loop_central_server_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestLoopCentralIsolation(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir_obj.name

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_game_roles_cannot_write_loop_central_ui_paths(self):
        guard = SafetyGuard(self.base_dir)

        self.assertFalse(guard.is_path_safe("ui/app.js", "developer"))
        self.assertFalse(guard.is_path_safe("ui/loop_central_server.py", "debug_dev"))
        self.assertTrue(guard.is_path_safe("public/index.html", "developer"))

    def test_new_sessions_do_not_expose_ui_workspace_root(self):
        state = SessionRouter(self.base_dir).create_session("Build a menu", "build_a_menu", kind="implementation")

        self.assertNotIn("ui", state["workspace_roots"])
        self.assertIn("public", state["workspace_roots"])

        harness_state = SessionRouter(self.base_dir).create_session(
            "Improve the Studio Loop harness", "improve_harness", kind="harness_upgrade"
        )
        self.assertIn(".agent/orchestrator", harness_state["workspace_roots"])
        self.assertNotIn("ui", harness_state["workspace_roots"])

    def test_local_audit_and_source_summary_ignore_loop_central_ui(self):
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "ui"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "src"), exist_ok=True)
        with open(os.path.join(self.base_dir, ".agent/Loop_Flow/source_index.json"), "w", encoding="utf-8") as handle:
            json.dump([
                {"path": "ui/app.js", "line_count": 10, "symbols": ["render"], "imports": []},
                {"path": "src/index.ts", "line_count": 5, "symbols": ["start"], "imports": []},
            ], handle)

        summary = SourceIndexer(self.base_dir).generate_context_summary()

        self.assertNotIn("ui/app.js", summary)
        self.assertIn("src/index.ts", summary)
        self.assertNotIn("ui", ResearchClient.ALLOWED_LOCAL_ROOTS)

    def test_kobold_client_writes_loop_central_logs_to_separate_directory(self):
        config = {
            "koboldcpp": {
                "base_url": "http://127.0.0.1:5001",
                "endpoint": "/v1/chat/completions",
                "model": "test",
                "temperature": 0,
                "top_p": 1,
                "max_output_tokens": 16,
            },
            "paths": {"logs": ".agent/logs"},
        }
        client = KoboldClient(config, base_path=self.base_dir)

        client.log_watch_interaction({"user": "prompt"}, "response", "20260513_000000")

        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "logs/loop_central/generations.jsonl")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "logs/loop_central/loop_central_state.json")))
        self.assertFalse(os.path.exists(os.path.join(self.base_dir, "logs/generations.jsonl")))
        self.assertFalse(os.path.exists(os.path.join(self.base_dir, "logs/harness_state.json")))

    def test_loop_central_snapshot_exposes_operator_controls(self):
        module = load_loop_central_module()
        central_dir = Path(self.base_dir) / "logs" / "loop_central"
        module.CENTRAL_DIR = central_dir
        module.KOBOLD_LOG = central_dir / "kobold.log"
        module.COMMAND_LOG = central_dir / "loop_central.log"
        module.GENERATIONS_LOG = central_dir / "generations.jsonl"
        module.CENTRAL_STATE = central_dir / "loop_central_state.json"
        module.AGENT_STATE = Path(self.base_dir) / ".agent" / "state" / "studio_loop_state.json"
        module.AGENT_RUN_LOGS = Path(self.base_dir) / ".agent" / "logs" / "orchestrator_runs"
        module.probe_kobold = lambda port: {"reachable": False, "base_url": f"http://127.0.0.1:{port}"}

        snapshot = module.build_snapshot(5001)

        self.assertIn("orchestrator", snapshot)
        self.assertIn("agent_state", snapshot)
        self.assertIn("continue", snapshot["orchestrator"]["commands"])
        self.assertIn("retry", snapshot["orchestrator"]["commands"])
        self.assertIn("central_log", snapshot["paths"])
        self.assertEqual(snapshot["paths"]["logs"], str(central_dir))


if __name__ == "__main__":
    unittest.main()
