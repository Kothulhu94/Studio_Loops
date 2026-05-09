import unittest
from unittest.mock import MagicMock, patch
import os
import json
import sys

# Add orchestrator to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator"))

from studio_loop import StudioLoopOrchestrator

class TestFullLoop(unittest.TestCase):
    def setUp(self):
        import tempfile
        import shutil
        self.original_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = os.path.join(self.temp_dir.name, "workspace")
        
        # Copy project to temp workspace, ignoring some bloat
        shutil.copytree(self.original_base_dir, self.base_dir, ignore=shutil.ignore_patterns('node_modules', '.git', '.agent/logs/*'))
        
        # Add orchestrator to path (from original to ensure imports work if not in temp)
        sys.path.append(os.path.join(self.original_base_dir, ".agent/orchestrator"))
        
        from studio_loop import StudioLoopOrchestrator
        self.orchestrator = StudioLoopOrchestrator(self.base_dir)
        
        # Mock client to avoid real model calls
        self.orchestrator.client.call = MagicMock()
        # Mock research to avoid real web requests
        self.orchestrator.research_client.perform_research = MagicMock()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_deterministic_loop(self):
        # 1. Concept Producer Response
        cp_response = {
            "actions": {
                "stage": "concept_producer",
                "status": "complete",
                "summary": "Concept for Feature X",
                "writes": [{"path": ".agent/Loop_Flow/implement_feature_x_blueprint.md", "content": "# Vision\nFeature X\n# Target User Experience\nFun\n# Thematic Alignment\nCool\n"}],
                "artifacts": [{"name": ".agent/Loop_Flow/implement_feature_x_blueprint.md", "type": "blueprint"}]
            }
        }
        
        # 2. Researcher Response
        res_response = {
            "actions": {
                "stage": "researcher",
                "status": "complete",
                "summary": "Research for Feature X",
                "writes": [
                    {"path": ".agent/Loop_Flow/implement_feature_x_blueprint.md", "content": "\n# Technical Audit\nUse patterns A and B.\n# Implementation Blueprint\nSteps...\n# Context Pruning Map\nMap...\n# Implementation Checklist\n- [ ] Task 1\n", "mode": "append"},
                    {"path": ".agent/Loop_Flow/context_map.json", "content": "{}"}
                ],
                "artifacts": [
                    {"name": ".agent/Loop_Flow/implement_feature_x_blueprint.md", "type": "blueprint"},
                    {"name": ".agent/Loop_Flow/context_map.json", "type": "context_map"}
                ],
                "research_requests": [{"query": "pattern A", "reason": "Implementation detail"}]
            }
        }
        
        # 3. Developer Response
        dev_response = {
            "actions": {
                "stage": "developer",
                "status": "complete",
                "summary": "Developer for Feature X",
                "writes": [
                    {"path": "src/feature_x.ts", "content": "export const x = 1;"},
                    {"path": "tests/feature_x.test.ts", "content": "import {x} from '../src/feature_x'; test('x', () => expect(x).toBe(1));"}
                ]
            }
        }
        
        # 4. QA Tester Response
        qa_response = {
            "actions": {
                "stage": "qa_tester",
                "status": "complete",
                "summary": "QA for Feature X",
                "qa_result": "PASS",
                "writes": [{"path": ".agent/Loop_Flow/implement_feature_x_qa_report.md", "content": "# Test Cases\nCase 1\n# Result\nPASS\n# Risks\nNone"}],
                "artifacts": [{"name": ".agent/Loop_Flow/implement_feature_x_qa_report.md", "type": "qa_report"}]
            }
        }

        # Sequence of model responses
        self.orchestrator.client.call.side_effect = [
            f"Thinking...\nACTIONS_JSON:\n{json.dumps(cp_response['actions'])}",
            f"Thinking...\nACTIONS_JSON:\n{json.dumps(res_response['actions'])}",
            f"Thinking...\nACTIONS_JSON:\n{json.dumps(res_response['actions'])}", # Second pass after research
            f"Thinking...\nACTIONS_JSON:\n{json.dumps(dev_response['actions'])}",
            f"Thinking...\nACTIONS_JSON:\n{json.dumps(qa_response['actions'])}"
        ]
        
        # Mock research return
        self.orchestrator.research_client.perform_research.return_value = {
            "status": "complete",
            "query": "pattern A",
            "findings": ["Pattern A found"],
            "sources": [{"title": "Source A", "url": "http://a.com", "status": "fetched"}],
            "artifact_path": ".agent/Loop_Flow/research/latest_pattern_a_research_brief.md"
        }
        
        # Mock test runner to succeed
        self.orchestrator.test_runner.run_full_suite = MagicMock(return_value={
            "typecheck": {"success": True},
            "tests": {"success": True},
            "bloat": {"success": True}
        })

        # Run autonomous loop
        self.orchestrator.run("Implement Feature X", mode="auto")
        
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["current_stage"], "handover_complete")
        print("PASS: Deterministic full-loop test successful.")

if __name__ == "__main__":
    unittest.main()
