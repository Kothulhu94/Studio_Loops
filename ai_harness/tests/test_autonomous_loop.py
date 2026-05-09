import unittest
import os
import json
import shutil
import sys
from unittest.mock import MagicMock, patch

# Add orchestrator to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))
from studio_loop import StudioLoopOrchestrator

class TestAutonomousLoop(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.original_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = os.path.join(self.temp_dir_obj.name, "workspace")
        
        # Copy project structure
        shutil.copytree(self.original_base_dir, self.temp_dir, ignore=shutil.ignore_patterns('node_modules', '.git', '.agent/logs/*'))
        
        self.orchestrator = StudioLoopOrchestrator(self.temp_dir)
        self.orchestrator.state_store.reset_state()
        self.blueprint_path = os.path.join(self.temp_dir, ".agent/Loop_Flow/test_feature_blueprint.md")
        
    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_research_to_blueprint_flow(self):
        """Tests a partial autonomous flow where a researcher requests research and then writes a blueprint."""
        
        # 1. Mock the Researcher's first response (requesting research)
        researcher_response_1 = """
        I need to research TypeScript Canvas patterns.
        
        ACTIONS_JSON:
        {
          "stage": "researcher",
          "status": "blocked",
          "summary": "Requesting research on Canvas patterns.",
          "research_requests": [
            { "query": "TypeScript Canvas game architecture patterns", "reason": "Need to establish base patterns." }
          ]
        }
        """
        
        # 2. Mock the Researcher's second response (completing after research)
        researcher_response_2 = """
        Research complete. Writing technical blueprint.
        
        ACTIONS_JSON:
        {
          "stage": "researcher",
          "status": "complete",
          "summary": "Technical blueprint for Canvas game established.",
          "writes": [
            { 
              "path": ".agent/Loop_Flow/test_feature_blueprint.md", 
              "content": "# Technical Blueprint\\n\\n## Technical Audit\\nDone.\\n\\n## Implementation Blueprint\\nPlan established.\\n\\n## Context Pruning Map\\n- src/main.ts\\n\\n## Implementation Checklist\\n- [ ] Task 1", 
              "mode": "overwrite" 
            }
          ],
          "next_stage_recommendation": "developer"
        }
        """
        
        import textwrap
        # 3. Mock the Kobold client to return our responses
        self.orchestrator.client.call = MagicMock(side_effect=[
            textwrap.dedent(researcher_response_1).strip(),
            textwrap.dedent(researcher_response_2).strip(),
            textwrap.dedent(researcher_response_2).strip()
        ])
        
        # 4. Mock the research client to return success without actually hitting the web
        self.orchestrator.research_client.browser_research.perform_research = MagicMock(return_value={
            "status": "complete",
            "query": "TypeScript Canvas game architecture patterns",
            "sources": [
                {"title": "Canvas API", "url": "https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API", "status": "fetched"},
                {"title": "Game Loop Patterns", "url": "https://gameprogrammingpatterns.com/game-loop.html", "status": "fetched"}
            ],
            "findings": ["Finding 1: Use a game loop.", "Finding 2: Separate update and render."],
            "artifact_path": os.path.join(self.temp_dir, ".agent/Loop_Flow/research/test_research.md")
        })
        
        # Start the feature
        self.orchestrator.state_store.start_feature("Test Feature", "test_feature", "researcher")
        
        # Execute the stage (should trigger two passes due to research)
        success = self.orchestrator.execute_stage("researcher")
        
        self.assertTrue(success)
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["current_stage"], "developer")
        self.assertIn("researcher", state["completed_stages"])
        self.assertTrue(os.path.exists(self.blueprint_path))

if __name__ == "__main__":
    unittest.main()
