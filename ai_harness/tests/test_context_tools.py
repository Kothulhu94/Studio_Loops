import json
import os
import shutil
import sys
import tempfile
import unittest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(REPO_ROOT)

from tools.context_report import build_report
from tools.replay_orchestrator_run import replay


class TestContextTools(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir_obj.name
        os.makedirs(os.path.join(self.base_dir, ".agent/orchestrator"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, ".agent/logs/orchestrator_runs"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, ".agent/logs/context_telemetry"), exist_ok=True)
        shutil.copy2(
            os.path.join(REPO_ROOT, ".agent/orchestrator/response_parser.py"),
            os.path.join(self.base_dir, ".agent/orchestrator/response_parser.py"),
        )
        shutil.copy2(
            os.path.join(REPO_ROOT, ".agent/orchestrator/actions_schema.json"),
            os.path.join(self.base_dir, ".agent/orchestrator/actions_schema.json"),
        )

        self.prompt_path = os.path.join(self.base_dir, ".agent/logs/orchestrator_runs/20260513_000000_prompt.json")
        self.response_path = os.path.join(self.base_dir, ".agent/logs/orchestrator_runs/20260513_000000_response.txt")
        prompt_user = (
            "# Studio Loop Stage Prompt\n\n"
            "## Context Map Validation\n"
            "- Status: valid\n"
            "- Target files: 1\n\n"
            "## Target Source Files\n"
            "### Target File: src/engine/Game.ts\n"
            "```\nexport class Game {}\n```\n"
        )
        with open(self.prompt_path, "w", encoding="utf-8") as handle:
            json.dump({
                "system": "test",
                "user": prompt_user,
                "telemetry": {
                    "stage": "developer",
                    "max_prompt_chars": 1000,
                    "raw_section_chars": {"context": 400},
                    "budgeted_section_chars": {"context": 250},
                    "truncations": [{"section": "context_pack", "from": 400, "to": 250}],
                    "final_user_chars": len(prompt_user),
                },
            }, handle)
        with open(self.response_path, "w", encoding="utf-8") as handle:
            handle.write(
                "ACTIONS_JSON:\n"
                "{\n"
                '  "stage": "developer",\n'
                '  "status": "complete",\n'
                '  "summary": "Implemented the target behavior.",\n'
                '  "writes": [],\n'
                '  "patches": [],\n'
                '  "commands": [],\n'
                '  "research_requests": []\n'
                "}\n"
            )

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_context_report_summarizes_prompt_telemetry(self):
        report = build_report(self.base_dir)

        self.assertEqual(report["stage"], "developer")
        self.assertEqual(report["target_files"], ["src/engine/Game.ts"])
        self.assertEqual(report["context_map_validation"]["status"], "valid")
        self.assertEqual(len(report["truncations"]), 1)
        self.assertFalse(report["middle_truncation_marker_found"])

    def test_replay_validates_logged_response_without_side_effects(self):
        report = replay(self.base_dir, self.prompt_path, self.response_path)

        self.assertTrue(report["parsed"])
        self.assertTrue(report["valid"], report["validation_error"])
        self.assertEqual(report["stage"], "developer")
        self.assertEqual(report["status"], "complete")
        self.assertEqual(report["target_files"], ["src/engine/Game.ts"])


if __name__ == "__main__":
    unittest.main()
