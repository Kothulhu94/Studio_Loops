import json
import os
import sys
import tempfile
import unittest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(REPO_ROOT, ".agent/orchestrator"))
sys.path.append(REPO_ROOT)

from context_pruner import ContextPruner
from prompt_compiler import PromptCompiler
from tools.context_culler import get_context_map


class TestContextBudgeting(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir_obj.name
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, ".agent/Loop_Flow/context_packs"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "src/engine"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "public"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "logs"), exist_ok=True)

        self.config = {
            "context_budget": {
                "max_prompt_chars": 12000,
                "state_chars": 1500,
                "role_instruction_chars": 1200,
                "skill_instruction_chars": 800,
                "active_artifact_chars": 1600,
                "target_source_chars": 5000,
                "pruned_context_chars": 6000,
            },
            "paths": {
                "loop_flow": ".agent/Loop_Flow",
            },
        }

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_prompt_budgeting_preserves_target_files_without_middle_truncation(self):
        compiler = PromptCompiler(self.config)
        state = {
            "session_id": "s1",
            "kind": "feature",
            "stack_profile": "game_source",
            "feature": "Implement start menu.",
            "feature_slug": "start_menu",
            "status": "running",
            "current_stage": "developer",
            "research_results": [
                {"stage": "developer", "query": "blocked old audit", "status": "blocked", "errors": ["missing"]},
            ],
            "failures": [{"stage": "developer", "reason": "Old failure " + ("x" * 2000)}],
            "blockers": [{"stage": "developer", "reason": "Old blocker " + ("y" * 2000)}],
        }
        context = (
            "# Context Pack: start_menu / developer\n\n"
            "## Feature Goal\nImplement start menu.\n\n"
            "## Target Source Files\n"
            "### Target File: src/engine/Game.ts\n"
            "```\nexport enum GameState { LOADING = 'LOADING', MAIN_MENU = 'MAIN_MENU' }\n```\n\n"
            "## Artifact Content\n" + ("artifact noise\n" * 1000) + "\n"
            "## Relevant Research Briefs\n" + ("research noise\n" * 1000) + "\n"
            "## Pruned Source Context\n" + ("source noise\n" * 1000)
        )

        prompt = compiler.compile_prompt(
            "developer",
            "Implement start menu.",
            "Implement start menu.",
            state,
            "workflow instructions\n" * 400,
            "skill instructions\n" * 400,
            context,
            {},
            [],
        )

        self.assertLessEqual(len(prompt["user"]), self.config["context_budget"]["max_prompt_chars"])
        self.assertNotIn("CONTEXT TRUNCATED BY ORCHESTRATOR", prompt["user"])
        self.assertIn("### Target File: src/engine/Game.ts", prompt["user"])
        self.assertIn("export enum GameState", prompt["user"])
        self.assertTrue(prompt["telemetry"]["truncations"])

    def test_context_pack_puts_target_files_before_artifacts_and_omits_blocked_research(self):
        with open(os.path.join(self.base_dir, "src/engine/Game.ts"), "w", encoding="utf-8") as handle:
            handle.write("export enum GameState { LOADING = 'LOADING' }\n")
        with open(os.path.join(self.base_dir, "public/index.html"), "w", encoding="utf-8") as handle:
            handle.write("<div id=\"app\"></div>\n")
        context_map_path = os.path.join(self.base_dir, ".agent/Loop_Flow/context_map.json")
        with open(context_map_path, "w", encoding="utf-8") as handle:
            json.dump({
                "target_files": [
                    {"path": "src/engine/Game.ts", "reason": "state"},
                    {"path": "public/index.html", "reason": "dom"},
                ]
            }, handle)

        pruner = ContextPruner(self.config, self.base_dir)
        pack_path = pruner.build_context_pack(
            "start_menu",
            "developer",
            "Implement start menu.",
            {
                "feature": "Implement start menu.",
                "stack_profile": "game_source",
                "artifacts": {"context_map.json": ".agent/Loop_Flow/context_map.json"},
                "research_results": [
                    {"query": "blocked local audit", "status": "blocked", "artifact_path": "blocked.md"},
                    {"query": "usable architecture research", "status": "complete", "findings": ["Use DOM state updates."]},
                ],
            },
        )
        with open(pack_path, encoding="utf-8") as handle:
            content = handle.read()

        self.assertLess(content.find("## Target Source Files"), content.find("## Artifact Content"))
        self.assertIn("These source files are already available", content)
        self.assertIn("## Context Map Validation", content)
        self.assertIn("- Status: valid", content)
        self.assertIn("### Target File: src/engine/Game.ts", content)
        self.assertIn("usable architecture research", content)
        self.assertNotIn("blocked local audit", content)

    def test_context_culler_ignores_logs_and_generated_noise(self):
        with open(os.path.join(self.base_dir, "src/engine/Game.ts"), "w", encoding="utf-8") as handle:
            handle.write("export const screenState = 'menu';\n")
        with open(os.path.join(self.base_dir, "logs/orchestrator_ui.log"), "w", encoding="utf-8") as handle:
            handle.write("screen screen screen\n")
        with open(os.path.join(self.base_dir, "debug_prompt.txt"), "w", encoding="utf-8") as handle:
            handle.write("screen screen screen\n")

        results = get_context_map(self.base_dir, ["screen"])

        self.assertIn("src/engine/Game.ts", results)
        self.assertNotIn("logs/orchestrator_ui.log", results)
        self.assertNotIn("debug_prompt.txt", results)


if __name__ == "__main__":
    unittest.main()
