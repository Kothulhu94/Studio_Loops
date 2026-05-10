import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import MagicMock


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from studio_loop import StudioLoopOrchestrator
from kobold_client import KoboldTransportError


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
        self.assertIn("REQUIRED ROOT SHAPE", repair_prompt_packet["user"])
        self.assertIn("ACTIONS_JSON:", repair_prompt_packet["user"])
        self.assertIn('"stage": "concept_producer"', repair_prompt_packet["user"])
        self.assertIn('"research_requests": []', repair_prompt_packet["user"])
        self.assertIn('Do not wrap it in {"actions": ...}', repair_prompt_packet["user"])
        self.assertIn("Do not return arrays at the root", repair_prompt_packet["user"])

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

    def test_post_execution_validation_failure_uses_repair_prompt_with_results(self):
        self.orchestrator.state_store.reset_state()
        self.orchestrator.state_store.start_feature(
            "Bad concept feature", "bad_concept_feature", "concept_producer", kind="design"
        )
        first_response = """
        ACTIONS_JSON:
        {
          "stage": "concept_producer",
          "status": "complete",
          "summary": "Concept blueprint written with missing required sections.",
          "qa_result": null,
          "writes": [
            {
              "path": ".agent/Loop_Flow/bad_concept_feature_blueprint.md",
              "content": "# Vision\\nOnly the vision exists.",
              "mode": "create"
            }
          ]
        }
        """
        repair_response = """
        ACTIONS_JSON:
        {
          "stage": "concept_producer",
          "status": "blocked",
          "summary": "Concept blueprint needs required sections repaired.",
          "qa_result": null,
          "blockers": [{"reason": "Required concept sections are missing."}]
        }
        """
        self.orchestrator.client.call = MagicMock(side_effect=[first_response, repair_response])

        success = self.orchestrator.execute_stage("concept_producer")

        self.assertFalse(success)
        self.assertEqual(self.orchestrator.client.call.call_count, 2)
        repair_prompt = self.orchestrator.client.call.call_args_list[1].args[0]["user"]
        self.assertIn("POST_EXECUTION_VALIDATION_FAILED", repair_prompt)
        self.assertIn("Required section", repair_prompt)
        self.assertIn("ACTION EXECUTION STATUS", repair_prompt)
        self.assertIn(".agent/Loop_Flow/bad_concept_feature_blueprint.md", repair_prompt)
        self.assertIn('"success": true', repair_prompt)
        self.assertIn('use mode="overwrite"', repair_prompt)

    def test_research_required_missing_repairs_before_writes(self):
        self.orchestrator.state_store.reset_state()
        self.orchestrator.state_store.start_feature(
            "Research required feature", "research_required_feature", "researcher", kind="research"
        )
        first_response = """
        ACTIONS_JSON:
        {
          "stage": "researcher",
          "status": "complete",
          "summary": "Technical blueprint written without required research.",
          "qa_result": null,
          "writes": [
            {
              "path": ".agent/Loop_Flow/research_required_feature_blueprint.md",
              "content": "# Technical Audit\\nAudit.\\n# Implementation Blueprint\\nPlan.\\n# Context Pruning Map\\nMap.\\n# Implementation Checklist\\n- [ ] One.",
              "mode": "create"
            }
          ]
        }
        """
        repair_response = """
        ACTIONS_JSON:
        {
          "stage": "researcher",
          "status": "blocked",
          "summary": "Research is required before writing the final technical blueprint.",
          "qa_result": null,
          "research_requests": [
            {
              "query": "TypeScript browser Vitest task queue data model best practices",
              "reason": "Ground the required technical blueprint in current TypeScript/browser/Vitest practice.",
              "required": true
            }
          ],
          "blockers": [{"reason": "Waiting for required research pass."}]
        }
        """
        self.orchestrator.client.call = MagicMock(side_effect=[first_response, repair_response])
        self.orchestrator.research_client.perform_research = MagicMock(return_value={
            "status": "blocked",
            "query": "TypeScript browser Vitest task queue data model best practices",
            "sources": [],
            "findings": [],
            "artifact_path": None,
            "errors": ["mocked research not performed"],
        })

        success = self.orchestrator.execute_stage("researcher")

        self.assertFalse(success)
        repair_prompt = self.orchestrator.client.call.call_args_list[1].args[0]["user"]
        self.assertIn("RESEARCH_REQUIRED_MISSING", repair_prompt)
        self.assertIn("Return status blocked with one or more research_requests", repair_prompt)
        self.assertIn("request research first", repair_prompt)
        self.assertIn("TypeScript/browser/Vitest", repair_prompt)
        self.assertFalse(
            os.path.exists(os.path.join(self.base_dir, ".agent/Loop_Flow/research_required_feature_blueprint.md"))
        )

    def test_harness_internal_repair_prompt_offers_discovery_audit(self):
        repair_prompt = self.orchestrator.retry_engine.get_repair_prompt(
            "VALIDATION_FAILED",
            "RESEARCH_REQUIRED_MISSING: This stage has research_required=true.",
            stage_name="researcher",
            stack_profile="harness_internal",
        )

        self.assertIn('audit_kind="discovery"', repair_prompt)
        self.assertIn('target_files [".agent", "tests", "tools"]', repair_prompt)
        self.assertIn('mode="local_codebase"', repair_prompt)

    def test_transport_timeout_does_not_trigger_schema_repair(self):
        self.orchestrator.state_store.reset_state()
        self.orchestrator.state_store.start_feature(
            "Transport failure feature", "transport_failure_feature", "researcher", kind="research"
        )
        self.orchestrator.client.call = MagicMock(side_effect=KoboldTransportError("read timed out"))
        self.orchestrator.repair_output = MagicMock()

        success = self.orchestrator.execute_stage("researcher")

        self.assertFalse(success)
        self.orchestrator.repair_output.assert_not_called()
        self.assertEqual(self.orchestrator.client.call.call_count, 1)
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["status"], "failed")
        self.assertIn("MODEL_TRANSPORT_ERROR", state["failures"][-1]["reason"])
        self.assertIn("No schema repair was attempted", state["failures"][-1]["reason"])


if __name__ == "__main__":
    unittest.main()
