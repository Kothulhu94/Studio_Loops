import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import MagicMock


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(REPO_ROOT, ".agent/orchestrator"))
sys.path.append(REPO_ROOT)

from artifact_validator import ArtifactValidator
from research_client import ResearchClient
from studio_loop import StudioLoopOrchestrator
from transition_engine import TransitionEngine


class TestLocalCodebaseAudit(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir_obj.name
        os.makedirs(os.path.join(self.base_dir, ".agent/orchestrator"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, ".agent/logs"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "tools"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "node_modules/pkg"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow/research"), exist_ok=True)
        self.sample_rel = ".agent/orchestrator/sample.py"
        with open(os.path.join(self.base_dir, self.sample_rel), "w", encoding="utf-8") as handle:
            handle.write(
                "import os\n"
                "from json import dumps\n\n"
                "class Sample:\n"
                "    def run(self):\n"
                "        return dumps({'ok': True})\n\n"
                "def integrate_with_state():\n"
                "    # TODO: refine integration\n"
                "    return os.getcwd()\n"
            )
        for rel_path, content in {
            ".agent/orchestrator/studio_loop.py": "class StudioLoopOrchestrator:\n    def execute_stage(self):\n        pass\n",
            ".agent/orchestrator/context_pruner.py": "class ContextPruner:\n    def prune(self):\n        pass\n",
            ".agent/orchestrator/context_compactor.py": "class ContextCompactor:\n    def compact(self):\n        pass\n",
            ".agent/logs/ignored.py": "class ShouldNotAppear:\n    pass\n",
            ".agent/Loop_Flow/generated.py": "class GeneratedArtifact:\n    pass\n",
            "node_modules/pkg/ignored.py": "class NodeModule:\n    pass\n",
        }.items():
            with open(os.path.join(self.base_dir, rel_path), "w", encoding="utf-8") as handle:
                handle.write(content)
        with open(os.path.join(self.base_dir, "tools/test_orchestrator.py"), "w", encoding="utf-8") as handle:
            handle.write("def test_orchestrator_helper():\n    return True\n")

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_local_audit_reads_temp_file_and_returns_complete_result(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)

        result = client.perform_research(
            "Audit sample.",
            "Need local evidence.",
            feature_slug="feature",
            stage="researcher",
            local_only=True,
            target_files=[self.sample_rel],
        )

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["evidence_type"], "local_codebase")
        self.assertEqual(result["backend"], "local_audit")
        self.assertTrue(result["source_set_relevance_passed"])
        self.assertGreaterEqual(len(result["findings"]), 2)
        self.assertEqual(result["sources"][0]["url"], f"local://{self.sample_rel}")
        self.assertTrue(os.path.exists(result["artifact_path"]))

    def test_local_discovery_accepts_agent_directory_and_returns_relevant_files(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)

        result = client.perform_research(
            "List all files and identify exact paths for StudioLoopOrchestrator ContextPruner ContextCompactor.",
            local_only=True,
            target_files=[".agent"],
            audit_kind="discovery",
        )

        findings = "\n".join(result["findings"])
        self.assertEqual(result["status"], "complete", result.get("errors"))
        self.assertEqual(result["audit_kind"], "discovery")
        self.assertIn(".agent/orchestrator/studio_loop.py", findings)
        self.assertIn(".agent/orchestrator/context_pruner.py", findings)
        self.assertIn(".agent/orchestrator/context_compactor.py", findings)
        self.assertNotIn(".agent/logs/ignored.py", findings)
        self.assertNotIn(".agent/Loop_Flow/generated.py", findings)
        self.assertNotIn("node_modules", findings)

    def test_local_file_audit_expands_safe_glob(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)

        result = client.perform_research(
            "Audit context files.",
            local_only=True,
            target_files=[".agent/orchestrator/context_*.py"],
        )

        urls = {source["url"] for source in result["sources"]}
        self.assertEqual(result["status"], "complete", result.get("errors"))
        self.assertIn("local://.agent/orchestrator/context_pruner.py", urls)
        self.assertIn("local://.agent/orchestrator/context_compactor.py", urls)

    def test_local_audit_blocks_when_target_file_missing(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)

        result = client.perform_research(
            "Audit missing file.",
            local_only=True,
            target_files=[".agent/orchestrator/missing.py"],
        )

        self.assertEqual(result["status"], "blocked")
        self.assertIn("does not exist", " ".join(result["errors"]))
        self.assertFalse(result["source_set_relevance_passed"])

    def test_local_audit_missing_test_path_suggests_tools_candidate(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)

        result = client.perform_research(
            "Audit mistaken test path.",
            local_only=True,
            target_files=["tests/test_orchestrator.py"],
        )

        self.assertEqual(result["status"], "blocked")
        self.assertIn("Target file does not exist: tests/test_orchestrator.py", " ".join(result["errors"]))
        self.assertIn("Closest candidate: tools/test_orchestrator.py", " ".join(result["errors"]))

    def test_local_audit_rejects_absolute_and_parent_paths(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)
        absolute_path = os.path.join(self.base_dir, self.sample_rel)

        result = client.perform_research(
            "Audit unsafe paths.",
            local_only=True,
            target_files=[absolute_path, "../outside.py"],
        )

        self.assertEqual(result["status"], "blocked")
        self.assertIn("workspace-relative", " ".join(result["errors"]))
        self.assertFalse(result["source_set_relevance_passed"])

    def test_local_audit_blocks_when_any_target_file_missing(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)

        result = client.perform_research(
            "Audit mixed files.",
            local_only=True,
            target_files=[self.sample_rel, ".agent/orchestrator/missing.py"],
        )

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(len(result["sources"]), 1)
        self.assertIn("does not exist", " ".join(result["errors"]))
        self.assertFalse(result["source_set_relevance_passed"])

    def test_artifact_validator_accepts_complete_local_codebase_result(self):
        client = ResearchClient({"web_research": {"artifact_dir": ".agent/Loop_Flow/research"}}, self.base_dir)
        result = client.perform_research("Audit sample.", local_only=True, target_files=[self.sample_rel])

        errors = ArtifactValidator(self.base_dir).validate_research_result(result)

        self.assertEqual(errors, [])

    def test_harness_upgrade_researcher_skips_designer_when_design_not_required(self):
        graph = MagicMock()
        graph.get_allowed_next.return_value = ["designer", "developer"]
        engine = TransitionEngine(graph)

        next_stage = engine.get_next_stage("researcher", {
            "status": "complete",
            "next_stage_recommendation": "designer",
            "design_required": False,
        }, {"valid": True})

        self.assertEqual(next_stage, "developer")

    def test_qa_skipped_without_blockers_completes_handover(self):
        graph = MagicMock()
        graph.get_allowed_next.return_value = ["bug_hunter", "handover_complete"]
        engine = TransitionEngine(graph)

        next_stage = engine.get_next_stage("qa_tester", {
            "status": "complete",
            "qa_result": "SKIPPED",
            "blockers": [],
        }, {"valid": True})

        self.assertEqual(next_stage, "handover_complete")

    def test_workflow_skill_cleanup_verifier_catches_legacy_terms(self):
        from tools import verify_clean_runtime

        dirty = []
        workflow_dir = os.path.join(self.base_dir, ".agent/workflows")
        os.makedirs(workflow_dir, exist_ok=True)
        with open(os.path.join(workflow_dir, "legacy.md"), "w", encoding="utf-8") as handle:
            handle.write("Use Gemistein Protocol and run_command.")

        verify_clean_runtime._verify_workflow_skill_terms(self.base_dir, dirty)

        self.assertTrue(any("Gemistein Protocol" in item for item in dirty))


class TestHarnessInternalAuditLoop(unittest.TestCase):
    def setUp(self):
        self.original_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = os.path.join(self.temp_dir_obj.name, "workspace")
        shutil.copytree(
            self.original_base_dir,
            self.base_dir,
            ignore=shutil.ignore_patterns("node_modules", ".git", ".agent/logs/*", ".agent/Loop_Flow/research/*"),
        )
        self.orchestrator = StudioLoopOrchestrator(self.base_dir)
        self.orchestrator.capability_registry.detect_all = MagicMock(return_value={"commands": {"typecheck": True}})

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_blocked_actions_with_research_requests_reenter_researcher(self):
        first = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Need local audit before technical blueprint.",
            "research_requests": [{
                "query": "Analyze ContextPruner and ContextCompactor implementations.",
                "reason": "Needed for harness_internal technical audit.",
                "required": True,
                "mode": "local_codebase",
                "target_files": [
                    ".agent/orchestrator/context_pruner.py",
                    ".agent/orchestrator/context_compactor.py",
                ],
            }],
        }
        second = {
            "stage": "researcher",
            "status": "complete",
            "summary": "Technical blueprint completed after local audit.",
            "design_required": False,
            "writes": [
                {
                    "path": ".agent/Loop_Flow/harness_test_blueprint.md",
                    "content": "# Technical Audit\nDone.\n# Implementation Blueprint\nPlan.\n# Context Pruning Map\nMap.\n# Implementation Checklist\n- [ ] Task\n",
                    "mode": "overwrite",
                },
                {"path": ".agent/Loop_Flow/context_map.json", "content": "{}", "mode": "overwrite"},
            ],
            "next_stage_recommendation": "designer",
        }
        self.orchestrator.client.call = MagicMock(side_effect=[
            f"ACTIONS_JSON:\n{json.dumps(first)}",
            f"ACTIONS_JSON:\n{json.dumps(second)}",
        ])

        self.orchestrator.state_store.start_feature(
            "Improve the Studio Loop harness by adding safer local audit.",
            "harness_test",
            "researcher",
            kind="harness_upgrade",
        )

        success = self.orchestrator.execute_stage("researcher")

        self.assertTrue(success)
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["current_stage"], "developer")
        self.assertNotEqual(state["status"], "blocked")
        self.assertTrue(any(r.get("evidence_type") == "local_codebase" and r.get("stage") == "researcher" for r in state["research_results"]))
        self.assertTrue(any(path.endswith("_research_brief.md") for path in state["research_briefs"]))

    def test_observed_local_codebase_request_shape_executes_and_records_complete_result(self):
        self.orchestrator.state_store.start_feature(
            "Improve the Studio Loop harness by adding safer local audit.",
            "observed_harness",
            "researcher",
            kind="harness_upgrade",
        )
        actions = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Need local audit before proceeding.",
            "design_required": False,
            "next_stage_recommendation": None,
            "research_requests": [{
                "query": "Audit local harness execution path.",
                "reason": "Needed for harness_internal technical audit.",
                "required": True,
                "mode": "local_codebase",
                "target_files": [
                    ".agent/orchestrator/studio_loop.py",
                    ".agent/orchestrator/research_client.py",
                    ".agent/orchestrator/transition_engine.py",
                    ".agent/orchestrator/artifact_validator.py",
                ],
            }],
        }

        results, research_performed = self.orchestrator.perform_actions("researcher", actions)

        self.assertTrue(research_performed)
        self.assertEqual(results["research"][0]["status"], "complete")
        self.assertEqual(results["research"][0]["evidence_type"], "local_codebase")
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["research_results"][0]["stage"], "researcher")
        self.assertEqual(state["research_results"][0]["status"], "complete")
        self.assertTrue(state["research_briefs"])

    def test_discovery_request_defers_dependent_local_audit_without_targets(self):
        self.orchestrator.state_store.start_feature(
            "Improve the Studio Loop harness by adding safer local audit.",
            "discovery_harness",
            "researcher",
            kind="harness_upgrade",
        )
        actions = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Need discovery before exact file audit.",
            "research_requests": [
                {
                    "query": "List all files within the .agent directory to identify exact paths.",
                    "reason": "Find exact files first.",
                    "required": True,
                    "mode": "local_codebase",
                    "audit_kind": "discovery",
                    "target_files": [".agent"],
                },
                {
                    "query": "Perform a technical audit using the discovered file paths.",
                    "reason": "Depends on discovery.",
                    "required": True,
                    "mode": "local_codebase",
                },
            ],
        }

        results, research_performed = self.orchestrator.perform_actions("researcher", actions)

        self.assertTrue(research_performed)
        self.assertEqual(len(results["research"]), 1)
        self.assertEqual(results["research"][0]["status"], "complete")
        self.assertEqual(results["research"][0].get("audit_kind"), "discovery")

    def test_complete_discovery_reenters_when_companion_local_audit_blocks(self):
        first = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Need discovery plus a follow-up local audit.",
            "research_requests": [
                {
                    "query": "List all files within the .agent directory to identify exact paths.",
                    "reason": "Find exact files first.",
                    "required": True,
                    "mode": "local_codebase",
                    "audit_kind": "discovery",
                    "target_files": [".agent"],
                },
                {
                    "query": "Audit the missing historical test path.",
                    "reason": "Verify path handling.",
                    "required": True,
                    "mode": "local_codebase",
                    "target_files": ["tests/test_orchestrator.py"],
                },
            ],
        }
        second = {
            "stage": "researcher",
            "status": "complete",
            "summary": "Technical blueprint completed after discovery.",
            "design_required": False,
            "writes": [
                {
                    "path": ".agent/Loop_Flow/mixed_discovery_blueprint.md",
                    "content": "# Technical Audit\nDone.\n# Implementation Blueprint\nPlan.\n# Context Pruning Map\nMap.\n# Implementation Checklist\n- [ ] Task\n",
                    "mode": "overwrite",
                },
                {"path": ".agent/Loop_Flow/context_map.json", "content": "{}", "mode": "overwrite"},
            ],
            "next_stage_recommendation": "designer",
        }
        self.orchestrator.client.call = MagicMock(side_effect=[
            f"ACTIONS_JSON:\n{json.dumps(first)}",
            f"ACTIONS_JSON:\n{json.dumps(second)}",
        ])

        self.orchestrator.state_store.start_feature(
            "Improve the Studio Loop harness by adding safer local audit.",
            "mixed_discovery_harness",
            "researcher",
            kind="harness_upgrade",
        )

        success = self.orchestrator.execute_stage("researcher")

        self.assertTrue(success)
        state = self.orchestrator.state_store.load_state()
        self.assertEqual(state["current_stage"], "developer")
        self.assertTrue(any(r.get("status") == "complete" and r.get("audit_kind") == "discovery" for r in state["research_results"]))
        self.assertTrue(any(r.get("status") == "blocked" and "tests/test_orchestrator.py" in r.get("errors", [""])[0] for r in state["research_results"]))

    def test_blocked_guessed_file_audit_records_discovery_fallback(self):
        self.orchestrator.state_store.start_feature(
            "Improve the Studio Loop harness by adding safer local audit.",
            "fallback_discovery_harness",
            "researcher",
            kind="harness_upgrade",
        )
        actions = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Need local audit but guessed exact paths.",
            "research_requests": [{
                "query": "Perform a local technical audit of the orchestrator architecture and transition engine.",
                "reason": "Map actual harness files.",
                "required": True,
                "mode": "local_codebase",
                "target_files": [
                    ".agent/orchestrator.py",
                    ".agent/graph/state_machine.py",
                ],
            }],
        }

        results, research_performed = self.orchestrator.perform_actions("researcher", actions)

        self.assertTrue(research_performed)
        self.assertEqual(results["research"][0]["status"], "blocked")
        self.assertEqual(results["research"][1]["status"], "complete")
        self.assertEqual(results["research"][1].get("audit_kind"), "discovery")
        self.assertTrue(any("studio_loop.py" in finding for finding in results["research"][1]["findings"]))

    def test_harness_internal_no_target_local_audit_defaults_to_discovery(self):
        self.orchestrator.state_store.start_feature(
            "Improve the Studio Loop harness by adding safer local audit.",
            "implicit_discovery_harness",
            "researcher",
            kind="harness_upgrade",
        )
        actions = {
            "stage": "researcher",
            "status": "blocked",
            "summary": "Need local codebase audit.",
            "research_requests": [{
                "query": "Local codebase audit of .agent orchestrator and skill systems",
                "reason": "Discover exact harness files.",
                "required": True,
            }],
        }

        results, research_performed = self.orchestrator.perform_actions("researcher", actions)

        self.assertTrue(research_performed)
        self.assertEqual(results["research"][0]["status"], "complete")
        self.assertEqual(results["research"][0].get("audit_kind"), "discovery")


if __name__ == "__main__":
    unittest.main()
