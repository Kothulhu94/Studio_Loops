import os
import sys
import json
import unittest
import shutil
from unittest.mock import MagicMock, patch

# Add orchestrator to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

try:
    from studio_loop import StudioLoopOrchestrator
except ImportError as e:
    print(f"FAILURE: Could not import orchestrator modules: {e}")
    sys.exit(1)

class TestStudioLoopOrchestrator(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.original_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = os.path.join(self.temp_dir_obj.name, "workspace")
        shutil.copytree(self.original_base_dir, self.temp_dir, ignore=shutil.ignore_patterns('node_modules', '.git', '.agent/logs/*'))
        
        self.orch = StudioLoopOrchestrator(self.temp_dir)
        self.orch.state_store.reset_state()

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_config_load(self):
        self.assertEqual(self.orch.config["koboldcpp"]["model"], "local-gemma-4")
        self.assertIn("web_research", self.orch.config)

    def test_state_init(self):
        state = self.orch.state_store.reset_state()
        self.assertEqual(state["status"], "idle")
        self.assertIsNone(state["current_stage"])

    def test_capability_detection(self):
        caps = self.orch.capability_registry.detect_all()
        self.assertIn("research", caps)
        self.assertIn("browser", caps)
        self.assertIn("web_search", caps["research"])

    def test_research_honesty(self):
        with patch('playwright_research.PlaywrightResearch.is_available', return_value=False):
            res = self.orch.research_client.perform_research("test query")
            self.assertEqual(res["status"], "blocked")
            self.assertIn("No functional browser research backend", res["errors"][0])

    def test_auto_loop_mock(self):
        self.orch.state_store.reset_state()
        self.orch.state_store.start_feature("Test Feature", "test_feature", "concept_producer")
        
        mock_response = "ACTIONS_JSON: " + json.dumps({
            "stage": "concept_producer",
            "summary": "Mocking concept production",
            "status": "complete",
            "next_stage_recommendation": "researcher",
            "writes": [{"path": ".agent/Loop_Flow/test_feature_blueprint.md", "content": "# Vision\nTest\n# Target User Experience\nTest\n# Thematic Alignment\nTest"}],
            "patches": []
        })
        
        with patch.object(self.orch.client, 'call', return_value=mock_response):
            with patch.object(self.orch.test_runner, 'run_typecheck', return_value={"success": True}):
                success = self.orch.execute_stage("concept_producer")
                self.assertTrue(success)
                
                state = self.orch.state_store.load_state()
                self.assertEqual(state["current_stage"], "researcher")
                self.assertTrue(any("test_feature_blueprint.md" in v for v in state["artifacts"].values()))

    def test_validation_failure(self):
        self.orch.state_store.reset_state()
        self.orch.state_store.start_feature("Test Feature", "test_feature", "concept_producer")
        
        mock_response = "ACTIONS_JSON: " + json.dumps({
            "stage": "concept_producer",
            "summary": "Mocking failure",
            "status": "complete",
            "writes": [{"path": ".agent/Loop_Flow/test_feature_blueprint.md", "content": "# Empty"}],
            "patches": []
        })
        
        with patch.object(self.orch.client, 'call', return_value=mock_response):
            with patch.object(self.orch.retry_engine, 'should_retry', return_value=False):
                with patch.object(self.orch.test_runner, 'run_typecheck', return_value={"success": True}):
                    success = self.orch.execute_stage("concept_producer")
                    self.assertFalse(success)

    def test_multistage_loop_mock(self):
        self.orch.state_store.reset_state()
        self.orch.state_store.start_feature("MultiStage Feature", "multi_feature", "concept_producer")
        
        concept_resp = "ACTIONS_JSON: " + json.dumps({
            "stage": "concept_producer", "status": "complete", "summary": "Concept done",
            "writes": [{"path": ".agent/Loop_Flow/multi_feature_blueprint.md", "content": "# Vision\nTest\n# Target User Experience\nTest\n# Thematic Alignment\nTest"}]
        })
        research_resp_req = "ACTIONS_JSON: " + json.dumps({
            "stage": "researcher", "status": "blocked", "summary": "Researching...",
            "research_requests": [{"query": "test query"}]
        })
        research_resp_done = "ACTIONS_JSON: " + json.dumps({
            "stage": "researcher", "status": "complete", "summary": "Research done",
            "next_stage_recommendation": "designer",
            "writes": [{"path": ".agent/Loop_Flow/context_map.json", "content": "{}"}, {"path": ".agent/Loop_Flow/multi_feature_blueprint.md", "content": "# Technical Audit\nTest\n# Implementation Blueprint\nTest\n# Context Pruning Map\nTest\n# Implementation Checklist\nTest", "mode": "append"}]
        })
        
        with patch.object(self.orch.client, 'call', side_effect=[concept_resp, research_resp_req, research_resp_done]):
            with patch.object(self.orch.test_runner, 'run_typecheck', return_value={"success": True}):
                self.orch.execute_stage("concept_producer")
                state = self.orch.state_store.load_state()
                self.assertEqual(state["current_stage"], "researcher")
                
                self.orch.execute_stage("researcher")
                state = self.orch.state_store.load_state()
                self.assertEqual(state["current_stage"], "researcher")
                
                self.orch.execute_stage("researcher")
                state = self.orch.state_store.load_state()
                self.assertEqual(state["current_stage"], "designer") 

if __name__ == "__main__":
    unittest.main()
