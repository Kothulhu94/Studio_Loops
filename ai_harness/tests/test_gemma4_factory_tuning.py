import os
import sys
import unittest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from prompt_compiler import PromptCompiler
from retry_engine import RetryEngine


class TestGemma4FactoryTuning(unittest.TestCase):
    def test_stage_prompt_includes_gemma4_freshness_and_actions_contract(self):
        compiler = PromptCompiler({})
        packet = compiler.compile_prompt(
            "developer",
            "Fresh API feature",
            "Use the latest browser API behavior",
            {"feature_slug": "fresh_api_feature"},
            "Role workflow text",
            "Role skills text",
            "Context pack text",
            {"actions_json_required": True},
            ["Functional Code", "Verification Results"],
        )

        self.assertIn("Gemma 4 through KoboldCPP", packet["system"])
        self.assertIn("native system role", packet["system"])
        self.assertIn("Gemma 4 Factory Tuning", packet["user"])
        self.assertIn("Freshness and Verification Protocol", packet["user"])
        self.assertIn("Current run date (UTC):", packet["user"])
        self.assertIn("request research before completing", packet["user"])
        self.assertIn("ACTIONS_JSON", packet["user"])
        self.assertNotIn("$current_date_utc", packet["user"])

    def test_repair_prompt_is_tuned_for_deterministic_gemma4_json_repair(self):
        prompt = RetryEngine().get_repair_prompt(
            "VALIDATION_FAILED",
            "RESEARCH_REQUIRED_MISSING: latest browser behavior is required",
            stage_name="researcher",
        )

        self.assertIn("GEMMA 4 REPAIR MODE", prompt)
        self.assertIn("deterministic JSON repair task", prompt)
        self.assertIn("For version-sensitive or current facts, request research", prompt)
        self.assertIn("Do not claim verification", prompt)
        self.assertIn("ACTIONS_JSON:", prompt)


if __name__ == "__main__":
    unittest.main()
