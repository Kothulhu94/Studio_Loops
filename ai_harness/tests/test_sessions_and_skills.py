import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from artifact_validator import ArtifactValidator
from safety_guard import SafetyGuard
from session_router import SessionRouter
from skill_registry import SkillRegistry
from state_store import StateStore


class TestSessionsAndSkills(unittest.TestCase):
    def setUp(self):
        self.original_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = os.path.join(self.temp_dir_obj.name, "workspace")
        shutil.copytree(
            self.original_base_dir,
            self.base_dir,
            ignore=shutil.ignore_patterns("node_modules", ".git", ".agent/logs/*", ".agent/state/sessions/*"),
        )
        self.state_store = StateStore(os.path.join(self.base_dir, ".agent/state/studio_loop_state.json"))

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_session_creation_and_active_pointer_compatibility(self):
        state = self.state_store.start_feature("Design the colony HUD", "design_the_colony_hud", "concept_producer", kind="design")

        self.assertTrue(state["session_id"])
        self.assertEqual(state["kind"], "design")
        self.assertEqual(state["current_stage"], "concept_producer")
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, ".agent/state/sessions", state["session_id"] + ".json")))

        with open(os.path.join(self.base_dir, ".agent/state/studio_loop_state.json"), "r", encoding="utf-8") as handle:
            pointer = json.load(handle)
        self.assertEqual(pointer["active_session_id"], state["session_id"])
        self.assertEqual(self.state_store.load_state()["session_id"], state["session_id"])

    def test_routing_by_request_kind(self):
        router = SessionRouter(self.base_dir)
        self.assertEqual(router.infer_kind("fix the crash on load"), "bug")
        self.assertEqual(router.route_initial_stage("fix the crash on load"), "bug_hunter")
        self.assertEqual(router.infer_kind("make a new sprite sheet"), "asset")
        self.assertEqual(router.route_initial_stage("research canvas input architecture"), "researcher")
        self.assertEqual(router.route_initial_stage("implement the save game migration"), "developer")

    def test_resume_and_archive_session(self):
        first = self.state_store.start_feature("Research pathfinding", "research_pathfinding", "researcher", kind="research")
        second = self.state_store.start_feature("Fix combat bug", "fix_combat_bug", "bug_hunter", kind="bug")

        resumed = self.state_store.resume_session(first["session_id"])
        self.assertEqual(resumed["session_id"], first["session_id"])
        self.assertEqual(self.state_store.load_state()["session_id"], first["session_id"])

        archived = self.state_store.archive_session(second["session_id"])
        self.assertEqual(archived["status"], "archived")

    def test_missing_active_session_file_recovers_full_state_shape(self):
        state = self.state_store.start_feature("Build the loading menu", "build_loading_menu", "developer", kind="implementation")
        session_path = os.path.join(self.base_dir, ".agent/state/sessions", state["session_id"] + ".json")
        os.remove(session_path)

        loaded = self.state_store.load_state()

        self.assertEqual(loaded["session_id"], state["session_id"])
        self.assertEqual(loaded["current_stage"], "developer")
        self.assertIn("context_packs", loaded)
        self.assertIn("artifacts", loaded)
        self.assertTrue(os.path.exists(session_path))

        self.state_store.record_context_pack("developer", "pack.md")
        loaded = self.state_store.load_state()
        self.assertEqual(loaded["context_packs"]["developer"], "pack.md")

    def test_two_sessions_keep_stage_artifacts_and_research_isolated(self):
        first = self.state_store.start_feature("Research pathfinding", "research_pathfinding", "researcher", kind="research")
        first["current_stage"] = "developer"
        first["artifacts"]["brief"] = ".agent/Loop_Flow/research_pathfinding_blueprint.md"
        first["research_results"].append({"query": "pathfinding", "status": "complete"})
        self.state_store.save_state(first)

        second = self.state_store.start_feature("Fix combat bug", "fix_combat_bug", "bug_hunter", kind="bug")
        second["artifacts"]["root_cause"] = ".agent/Loop_Flow/fix_combat_bug_root_cause_analysis.md"
        self.state_store.save_state(second)

        loaded_first = self.state_store.get_session(first["session_id"])
        loaded_second = self.state_store.get_session(second["session_id"])
        self.assertEqual(loaded_first["current_stage"], "developer")
        self.assertEqual(loaded_second["current_stage"], "bug_hunter")
        self.assertEqual(len(loaded_first["research_results"]), 1)
        self.assertEqual(loaded_second["research_results"], [])
        self.assertNotEqual(loaded_first["artifacts"], loaded_second["artifacts"])

    def test_skill_registry_loads_trusted_and_rejects_external_by_default(self):
        registry = SkillRegistry(self.base_dir)
        developer_skills = registry.get_role_skills("developer")
        self.assertEqual([skill["id"] for skill in developer_skills], ["studio-loop.developer"])
        self.assertIn("src", registry.allowed_write_paths_for_role("developer"))

        external_dir = os.path.join(self.base_dir, ".agent/skills/external_test")
        os.makedirs(external_dir, exist_ok=True)
        manifest = {
            "id": "external.test",
            "name": "External Test",
            "version": "1.0.0",
            "roles": ["developer"],
            "required_tools": [],
            "allowed_write_paths": ["."],
            "expected_artifacts": [],
            "validators": [],
            "provenance": {"source": "test"},
            "trust_level": "external",
        }
        with open(os.path.join(external_dir, "skill.json"), "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        with open(os.path.join(self.base_dir, ".agent/skills/registry.json"), "r", encoding="utf-8") as handle:
            data = json.load(handle)
        data["skills"].append({"id": "external.test", "manifest": ".agent/skills/external_test/skill.json"})
        with open(os.path.join(self.base_dir, ".agent/skills/registry.json"), "w", encoding="utf-8") as handle:
            json.dump(data, handle)

        registry = SkillRegistry(self.base_dir)
        self.assertNotIn("external.test", [skill["id"] for skill in registry.get_role_skills("developer")])

    def test_skill_registry_rejects_invalid_manifest(self):
        registry = SkillRegistry(self.base_dir)
        invalid_path = os.path.join(self.base_dir, ".agent/skills/invalid_skill.json")
        with open(invalid_path, "w", encoding="utf-8") as handle:
            json.dump({"id": "broken"}, handle)
        with self.assertRaises(ValueError):
            registry.load_manifest(invalid_path)

    def test_safety_guard_uses_skill_policy(self):
        guard = SafetyGuard(self.base_dir)
        guard.set_policy_context({"designer": [".agent/Loop_Flow"]}, [".agent/Loop_Flow", "src"])

        safe, err = guard.validate_actions("designer", {
            "stage": "designer",
            "status": "complete",
            "summary": "Writes design spec.",
            "writes": [{"path": ".agent/Loop_Flow/test_design_spec.md", "content": "ok"}],
        })
        self.assertTrue(safe, err)

        safe, err = guard.validate_actions("designer", {
            "stage": "designer",
            "status": "complete",
            "summary": "Attempts source write.",
            "writes": [{"path": "src/ui.ts", "content": "bad"}],
        })
        self.assertFalse(safe)
        self.assertIn("Unsafe write path", err)

    def test_artifact_validator_uses_skill_expected_artifacts(self):
        validator = ArtifactValidator(self.base_dir)
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow"), exist_ok=True)
        path = os.path.join(self.base_dir, ".agent/Loop_Flow/test_feature_design_spec.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("# Aesthetic Spec\nOk\n# Interaction Spec\nOk\n# CSS Tokens\nOk\n")

        manifest = {
            "id": "test.designer",
            "expected_artifacts": [
                {
                    "path": ".agent/Loop_Flow/{feature}_design_spec.md",
                    "required": True,
                    "required_sections": ["Aesthetic Spec", "Interaction Spec", "CSS Tokens"],
                }
            ],
            "validators": [],
        }
        report = validator.validate(
            "designer",
            {"stage": "designer", "status": "complete", "summary": "Done"},
            {"writes": [], "patches": [], "commands": [], "research": []},
            {},
            {"feature_slug": "test_feature", "research_results": []},
            skill_manifests=[manifest],
        )
        self.assertTrue(report["valid"], report["errors"])

    def test_artifact_validator_accepts_written_technical_blueprint_for_researcher(self):
        validator = ArtifactValidator(self.base_dir)
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow"), exist_ok=True)
        concept_path = os.path.join(self.base_dir, ".agent/Loop_Flow/test_feature_blueprint.md")
        technical_path = os.path.join(self.base_dir, ".agent/Loop_Flow/test_feature_technical_blueprint.md")
        with open(concept_path, "w", encoding="utf-8") as handle:
            handle.write("# Vision\nConcept only.\n# Target User Experience\nOk\n# Thematic Alignment\nOk\n")
        with open(technical_path, "w", encoding="utf-8") as handle:
            handle.write(
                "# Technical Blueprint\n"
                "## Technical Audit\nOk\n"
                "## Implementation Blueprint\nOk\n"
                "## Context Pruning Map\nOk\n"
                "## Implementation Checklist\n- [ ] Ok\n"
            )

        actions = {
            "stage": "researcher",
            "status": "complete",
            "summary": "Researcher wrote a valid technical blueprint.",
            "writes": [
                {
                    "path": ".agent/Loop_Flow/test_feature_technical_blueprint.md",
                    "content": "",
                }
            ],
            "artifacts": [
                {
                    "name": "test_feature_technical_blueprint.md",
                    "type": "blueprint",
                }
            ],
        }
        results = {
            "writes": [
                {
                    "path": ".agent/Loop_Flow/test_feature_technical_blueprint.md",
                    "success": True,
                    "error": None,
                }
            ],
            "patches": [],
            "commands": [],
            "research": [],
        }
        rules = {
            "required_files": [".agent/Loop_Flow/{feature}_blueprint.md"],
            "required_sections": [
                "Technical Audit",
                "Implementation Blueprint",
                "Context Pruning Map",
                "Implementation Checklist",
            ],
        }
        manifest = {
            "id": "studio-loop.researcher",
            "expected_artifacts": [
                {
                    "path": ".agent/Loop_Flow/{feature}_blueprint.md",
                    "required": True,
                    "required_sections": rules["required_sections"],
                }
            ],
            "validators": [],
        }

        report = validator.validate(
            "researcher",
            actions,
            results,
            rules,
            {"feature_slug": "test_feature", "research_results": []},
            skill_manifests=[manifest],
        )

        self.assertTrue(report["valid"], report["errors"])


if __name__ == "__main__":
    unittest.main()
