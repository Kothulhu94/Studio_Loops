import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import MagicMock


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from studio_loop import StudioLoopOrchestrator


class TestRepairPrompt(unittest.TestCase):
    def setUp(self):
        self.original_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = os.path.join(self.temp_dir_obj.name, "workspace")
        shutil.copytree(
            self.original_base_dir,
            self.base_dir,
            ignore=shutil.ignore_patterns("node_modules", ".git", ".agent/logs/*", "__pycache__"),
        )
        self.orchestrator = StudioLoopOrchestrator(self.base_dir)
        self.orchestrator.state_store.reset_state()
        self.orchestrator.state_store.start_feature("Repair test feature", "repair_test_feature", "concept_producer")

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_repair_override_uses_prompt_packet_accepted_by_client_call(self):
        invalid_response = """
        ACTIONS_JSON:
        {
          "stage": "concept_producer",
          "status": "complete",
          "summary": "This response has an invalid QA result.",
          "qa_result": "WRONG"
        }
        """
        repaired_actions = {
            "stage": "concept_producer",
            "status": "blocked",
            "summary": "Repair path returned valid blocked actions.",
            "qa_result": None,
            "blockers": [{"reason": "Stopping after repair validation for test."}],
        }
        repaired_response = f"ACTIONS_JSON:\n{json.dumps(repaired_actions)}"
        self.orchestrator.client.call = MagicMock(side_effect=[invalid_response, repaired_response])

        success = self.orchestrator.execute_stage("concept_producer")

        self.assertFalse(success)
        self.assertEqual(self.orchestrator.client.call.call_count, 2)
        repair_prompt_packet = self.orchestrator.client.call.call_args_list[1].args[0]
        self.assertIsInstance(repair_prompt_packet, dict)
        self.assertIn("system", repair_prompt_packet)
        self.assertIn("user", repair_prompt_packet)
        self.assertIn("You are repairing the previous ACTIONS_JSON", repair_prompt_packet["system"])
        self.assertIn("concept_producer", repair_prompt_packet["user"])
        self.assertIn("Schema validation failed", repair_prompt_packet["user"])
        self.assertIn("invalid QA result", repair_prompt_packet["user"])
        self.assertIn("Return exactly one ACTIONS_JSON block", repair_prompt_packet["user"])
        self.assertIn('Use null as JSON null, not "null"', repair_prompt_packet["user"])
        self.assertIn("Do not invent writes/patches", repair_prompt_packet["user"])
        self.assertIn("Replace invalid values such as running", repair_prompt_packet["user"])
        self.assertIn("Do not wrap JSON in Markdown fences", repair_prompt_packet["user"])
        self.assertIn("Use next_stage_recommendation, not next_stage", repair_prompt_packet["user"])

    def test_running_status_triggers_repair_and_fenced_valid_repair_is_accepted(self):
        self.orchestrator.state_store.reset_state()
        self.orchestrator.state_store.start_feature(
            "Research test feature", "research_test_feature", "researcher", kind="research"
        )
        self.orchestrator.client.call = MagicMock(side_effect=[
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "running",
              "summary": "Trying to begin research with an invalid status."
            }
            """,
            """```json
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Research is needed before technical handoff can complete.",
              "qa_result": null,
              "blockers": [{"reason": "External research required."}]
            }
            ```""",
        ])

        success = self.orchestrator.execute_stage("researcher")

        self.assertFalse(success)
        self.assertEqual(self.orchestrator.client.call.call_count, 2)
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["current_stage"], "researcher")
        self.assertEqual(state["status"], "blocked")

    def test_repeated_invalid_repairs_persist_failure_on_current_stage(self):
        self.orchestrator.state_store.reset_state()
        self.orchestrator.state_store.start_feature(
            "Research failure feature", "research_failure_feature", "researcher", kind="research"
        )
        invalid_response = """
        ACTIONS_JSON:
        {
          "stage": "researcher",
          "status": "running",
          "summary": "Invalid status should exhaust repair attempts."
        }
        """
        self.orchestrator.client.call = MagicMock(return_value=invalid_response)

        success = self.orchestrator.execute_stage("researcher")

        self.assertFalse(success)
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["current_stage"], "researcher")
        self.assertEqual(state["status"], "failed")
        self.assertTrue(state["failures"])
        self.assertEqual(state["failures"][-1]["stage"], "researcher")
        self.assertIn("ACTIONS_JSON validation failed after repair retries", state["failures"][-1]["reason"])


if __name__ == "__main__":
    unittest.main()
