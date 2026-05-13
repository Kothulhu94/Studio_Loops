import os
import sys
import unittest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from response_parser import ResponseParser

class TestParserRobustness(unittest.TestCase):
    def setUp(self):
        self.schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../.agent/orchestrator/actions_schema.json")
        )
        self.parser = ResponseParser(schema_path=self.schema_path)

    def test_status_normalization(self):
        test_cases = [
            ("running", "blocked"),
            ("in_progress", "blocked"),
            ("working", "blocked"),
            ("success", "complete"),
            ("done", "complete"),
            ("error", "failed")
        ]
        
        for input_status, expected_status in test_cases:
            parsed = self.parser.parse(f'ACTIONS_JSON: {{"stage": "developer", "status": "{input_status}", "summary": "Test summary of at least 10 chars."}}')
            self.parser.normalize_actions(parsed["actions"])
            self.assertEqual(parsed["actions"]["status"], expected_status, f"Failed to normalize {input_status}")

    def test_marker_robustness(self):
        test_cases = [
            ("ACTIONS_JSON {", True),
            ("actions_json: {", True),
            ("Actions_Json {", True),
            ("No marker but valid shape", False) # Fallback should catch it though
        ]
        
        for marker_text, should_find in test_cases:
            if "{" in marker_text:
                text = f"{marker_text} \"stage\": \"developer\", \"status\": \"complete\", \"summary\": \"Valid summary text here.\" }}"
            else:
                text = f"{marker_text} {{ \"stage\": \"developer\", \"status\": \"complete\", \"summary\": \"Valid summary text here.\" }}"
            parsed = self.parser.parse(text)
            if should_find:
                self.assertIsNotNone(parsed["actions"], f"Failed to find marker: {marker_text}")
            else:
                self.assertIsNotNone(parsed["actions"], f"Should have found via fallback: {marker_text}")

    def test_marker_inside_json_robustness(self):
        # Gemma 4 sometimes puts the marker as a key inside the JSON
        text = """
        {
          "ACTIONS_JSON": {
            "stage": "developer",
            "status": "complete",
            "summary": "Marker is inside the JSON as a key."
          }
        }
        """
        parsed = self.parser.parse(text)
        self.assertIsNotNone(parsed["actions"])
        self.assertEqual(parsed["actions"]["summary"], "Marker is inside the JSON as a key.")

if __name__ == "__main__":
    unittest.main()
