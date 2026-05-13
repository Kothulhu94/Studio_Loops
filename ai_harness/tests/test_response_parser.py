import os
import sys
import unittest
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from response_parser import ResponseParser


class TestResponseParser(unittest.TestCase):
    def setUp(self):
        self.schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../.agent/orchestrator/actions_schema.json")
        )
        self.parser = ResponseParser(schema_path=self.schema_path)

    def test_qa_result_string_null_is_normalized_before_validation(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "concept_producer",
              "status": "complete",
              "summary": "Valid concept summary.",
              "qa_result": "null"
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertIsNone(parsed["actions"]["qa_result"])

    def test_qa_result_json_null_validates(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "concept_producer",
              "status": "complete",
              "summary": "Valid concept summary.",
              "qa_result": null
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertIsNone(parsed["actions"]["qa_result"])

    def test_actions_json_marker_still_parses_normally(self):
        parsed = self.parser.parse(
            """
            Some useful text.
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Blocked while requesting external research."
            }
            """
        )

        self.assertEqual(parsed["actions"]["stage"], "researcher")
        self.assertEqual(parsed["actions"]["status"], "blocked")

    def test_fenced_repair_json_without_marker_parses_if_action_shaped(self):
        parsed = self.parser.parse(
            """```json
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Blocked while requesting external research.",
              "qa_result": null
            }
            ```"""
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["stage"], "researcher")

    def test_fallback_rejects_unrelated_json_object(self):
        parsed = self.parser.parse('{"message": "not an action"}')

        self.assertIsNone(parsed["actions"])

    def test_unwraps_uppercase_actions_json_wrapper_if_inner_is_action_shaped(self):
        parsed = self.parser.parse(
            json.dumps({
                "ACTIONS_JSON": {
                    "stage": "researcher",
                    "status": "blocked",
                    "summary": "Wrapped response is safely unwrapped."
                }
            })
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["stage"], "researcher")

    def test_unwraps_lowercase_actions_json_wrapper_if_inner_is_action_shaped(self):
        parsed = self.parser.parse(
            json.dumps({
                "actions_json": {
                    "stage": "researcher",
                    "status": "blocked",
                    "summary": "Lowercase wrapped response is safely unwrapped."
                }
            })
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["status"], "blocked")

    def test_rejects_actions_array_wrapper_as_not_equivalent(self):
        parsed = self.parser.parse(
            'ACTIONS_JSON: {"actions": [], "status": "blocked", "summary": "Wrong root shape."}'
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertFalse(valid)
        self.assertIn("root shape is rejected", error)

    def test_invalid_running_status_is_normalized_to_blocked(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "running",
              "summary": "This should be normalized to blocked."
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["status"], "blocked")

    def test_next_stage_is_normalized_to_next_stage_recommendation(self):
        legacy_actions = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Blocked while requesting external research.",
            "next_stage": "developer",
        }
        good_actions = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Blocked while requesting external research.",
            "next_stage_recommendation": "developer",
        }

        legacy_copy = json.loads(json.dumps(legacy_actions))
        legacy_valid, legacy_error = self.parser.validate_actions(legacy_copy)
        good_valid, good_error = self.parser.validate_actions(json.loads(json.dumps(good_actions)))

        self.assertTrue(legacy_valid, legacy_error)
        self.assertNotIn("next_stage", legacy_copy)
        self.assertEqual(legacy_copy["next_stage_recommendation"], "developer")
        self.assertTrue(good_valid, good_error)

    def test_command_strings_are_normalized_to_allowlist_names(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "developer",
              "status": "blocked",
              "summary": "Requesting verification commands.",
              "commands": ["npm run typecheck", {"command": "npx vitest run", "args": {"bad": "shape"}}]
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["commands"][0]["name"], "typecheck")
        self.assertEqual(parsed["actions"]["commands"][1]["name"], "test")
        self.assertNotIn("args", parsed["actions"]["commands"][1])

    def test_research_request_topic_stack_is_normalized_to_schema_shape(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Requesting TypeScript browser architecture research.",
              "research_requests": [
                {
                  "topic": "TypeScript browser task queue data model Vitest unit test",
                  "stack": "TypeScript/browser/Vitest"
                }
              ]
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        request = parsed["actions"]["research_requests"][0]
        self.assertEqual(request["query"], "TypeScript browser task queue data model Vitest unit test")
        self.assertIn("TypeScript/browser/Vitest", request["reason"])
        self.assertNotIn("topic", request)
        self.assertNotIn("stack", request)

    def test_research_request_constraints_are_folded_into_reason(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Requesting constrained TypeScript browser architecture research.",
              "research_requests": [
                {
                  "query": "TypeScript browser task queue data model Vitest unit test",
                  "reason": "Need implementation references.",
                  "constraints": "Use browser/Vitest sources only."
                }
              ]
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        request = parsed["actions"]["research_requests"][0]
        self.assertIn("Need implementation references.", request["reason"])
        self.assertIn("Use browser/Vitest sources only.", request["reason"])
        self.assertNotIn("constraints", request)

    def test_string_research_request_is_normalized(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "String request.",
              "research_requests": ["audit local codebase"]
            }
            """
        )
        valid, error = self.parser.validate_actions(parsed["actions"])
        self.assertTrue(valid, error)
        req = parsed["actions"]["research_requests"][0]
        self.assertEqual(req["query"], "audit local codebase")
        self.assertEqual(req["required"], True)

    def test_blocker_string_is_normalized(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "This is a sufficiently long summary for blockers.",
              "blockers": ["Waiting for user input"]
            }
            """
        )
        valid, error = self.parser.validate_actions(parsed["actions"])
        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["blockers"][0]["reason"], "Waiting for user input")

    def test_invalid_next_stage_recommendation_is_corrected(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "complete",
              "summary": "This is a sufficiently long summary for next stage.",
              "next_stage_recommendation": "architect"
            }
            """
        )
        valid, error = self.parser.validate_actions(parsed["actions"])
        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["next_stage_recommendation"], "developer")

    def test_unknown_research_request_fields_are_dropped(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Noisy request.",
              "research_requests": [
                {
                  "query": "test",
                  "noise": "should be dropped",
                  "topic": "already handled but should be gone"
                }
              ]
            }
            """
        )
        valid, error = self.parser.validate_actions(parsed["actions"])
        self.assertTrue(valid, error)
        req = parsed["actions"]["research_requests"][0]
        self.assertNotIn("noise", req)
        self.assertNotIn("topic", req)

    def test_research_request_description_target_files_normalizes_to_local_codebase(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Requesting a local codebase audit.",
              "research_requests": [
                {
                  "description": "Analyze ContextPruner and ContextCompactor.",
                  "reason": "Needed for harness audit.",
                  "required": true,
                  "target_files": [
                    ".agent/orchestrator/context_pruner.py",
                    ".agent/orchestrator/context_compactor.py"
                  ],
                  "extra": "drop me"
                }
              ]
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        req = parsed["actions"]["research_requests"][0]
        self.assertEqual(req["query"], "Analyze ContextPruner and ContextCompactor.")
        self.assertEqual(req["mode"], "local_codebase")
        self.assertEqual(len(req["target_files"]), 2)
        self.assertNotIn("extra", req)

    def test_schema_accepts_local_codebase_mode_and_target_files(self):
        actions = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Requesting local audit with explicit mode.",
            "research_requests": [{
                "query": "Analyze orchestrator files.",
                "reason": "Needed for harness audit.",
                "required": True,
                "mode": "local_codebase",
                "audit_kind": "file_audit",
                "target_files": [".agent/orchestrator/studio_loop.py"]
            }]
        }

        valid, error = self.parser.validate_actions(actions)

        self.assertTrue(valid, error)

    def test_research_request_evidence_type_local_codebase_converts_to_mode(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "blocked",
              "summary": "Requesting local discovery.",
              "research_requests": [
                {
                  "description": "List all files within the .agent directory to identify exact paths.",
                  "evidence_type": "local_codebase",
                  "target_files": [".agent"],
                  "unknown": "drop"
                }
              ]
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        req = parsed["actions"]["research_requests"][0]
        self.assertEqual(req["mode"], "local_codebase")
        self.assertEqual(req["audit_kind"], "discovery")
        self.assertEqual(req["target_files"], [".agent"])
        self.assertNotIn("evidence_type", req)
        self.assertNotIn("unknown", req)

    def test_artifact_paths_normalize_to_schema_objects(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "complete",
              "summary": "Researcher wrote required artifacts.",
              "artifacts": [
                ".agent/Loop_Flow/context_map.json",
                {
                  "path": ".agent/Loop_Flow/sample_blueprint.md",
                  "type": "markdown",
                  "extra": "drop"
                }
              ]
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertTrue(valid, error)
        self.assertEqual(parsed["actions"]["artifacts"][0], {"name": "context_map.json", "type": "context_map"})
        self.assertEqual(parsed["actions"]["artifacts"][1], {"name": "sample_blueprint.md", "type": "markdown"})


if __name__ == "__main__":
    unittest.main()
