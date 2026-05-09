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

    def test_invalid_running_status_still_fails_schema_validation(self):
        parsed = self.parser.parse(
            """
            ACTIONS_JSON:
            {
              "stage": "researcher",
              "status": "running",
              "summary": "This should fail validation."
            }
            """
        )

        valid, error = self.parser.validate_actions(parsed["actions"])

        self.assertFalse(valid)
        self.assertIn("running", error)

    def test_next_stage_rejected_and_next_stage_recommendation_accepted(self):
        bad_actions = {
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

        bad_valid, bad_error = self.parser.validate_actions(json.loads(json.dumps(bad_actions)))
        good_valid, good_error = self.parser.validate_actions(json.loads(json.dumps(good_actions)))

        self.assertFalse(bad_valid)
        self.assertIn("Additional properties", bad_error)
        self.assertTrue(good_valid, good_error)


if __name__ == "__main__":
    unittest.main()
