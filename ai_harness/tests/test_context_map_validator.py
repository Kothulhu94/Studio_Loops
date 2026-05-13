import json
import os
import sys
import tempfile
import unittest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(REPO_ROOT, ".agent/orchestrator"))

from context_map_validator import ContextMapValidator


class TestContextMapValidator(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir_obj.name
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, ".agent/orchestrator"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "src/engine"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "public"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "ui"), exist_ok=True)
        with open(os.path.join(self.base_dir, "src/engine/Game.ts"), "w", encoding="utf-8") as handle:
            handle.write("export class Game {}\n")
        with open(os.path.join(self.base_dir, "public/index.html"), "w", encoding="utf-8") as handle:
            handle.write("<main></main>\n")
        with open(os.path.join(self.base_dir, "ui/app.js"), "w", encoding="utf-8") as handle:
            handle.write("console.log('watch');\n")
        with open(os.path.join(self.base_dir, ".agent/orchestrator/studio_loop.py"), "w", encoding="utf-8") as handle:
            handle.write("class StudioLoopOrchestrator: pass\n")
        self.validator = ContextMapValidator(self.base_dir)

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def write_context_map(self, payload):
        path = os.path.join(self.base_dir, ".agent/Loop_Flow/context_map.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        return ".agent/Loop_Flow/context_map.json"

    def test_normalizes_legacy_files_key_to_target_files(self):
        rel_path = self.write_context_map({
            "files": [{"path": "src/engine/Game.ts", "description": "core state"}],
        })

        result = self.validator.validate_file(rel_path, stack_profile="game_source", repair=True)

        self.assertTrue(result.valid, result.errors)
        self.assertTrue(result.changed)
        self.assertEqual(result.target_files[0]["path"], "src/engine/Game.ts")
        with open(os.path.join(self.base_dir, rel_path), encoding="utf-8") as handle:
            normalized = json.load(handle)
        self.assertIn("target_files", normalized)
        self.assertNotIn("files", normalized)

    def test_rejects_watch_ui_for_game_source_context(self):
        rel_path = self.write_context_map({
            "target_files": [{"path": "ui/app.js", "reason": "watch surface"}],
        })

        result = self.validator.validate_file(rel_path, stack_profile="game_source", repair=False)

        self.assertFalse(result.valid)
        self.assertIn("outside allowed context roots", "\n".join(result.errors))

    def test_promotes_exact_paths_from_artifact_text(self):
        rel_path = self.write_context_map({"feature_slug": "menu"})

        result = self.validator.validate_file(
            rel_path,
            stack_profile="game_source",
            candidate_text="Implement public/index.html and src/engine/Game.ts.",
            repair=False,
        )

        self.assertTrue(result.valid, result.errors)
        self.assertEqual(
            [item["path"] for item in result.target_files],
            ["public/index.html", "src/engine/Game.ts"],
        )
        self.assertTrue(result.warnings)

    def test_allows_harness_roots_for_harness_internal_context(self):
        rel_path = self.write_context_map({
            "target_files": [{"path": ".agent/orchestrator/studio_loop.py", "reason": "orchestrator"}],
        })

        result = self.validator.validate_file(rel_path, stack_profile="harness_internal", repair=False)

        self.assertTrue(result.valid, result.errors)
        self.assertEqual(result.target_files[0]["path"], ".agent/orchestrator/studio_loop.py")


if __name__ == "__main__":
    unittest.main()
