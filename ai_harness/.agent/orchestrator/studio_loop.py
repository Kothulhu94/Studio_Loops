import sys
import os
import json
import argparse
from datetime import datetime

# Add the current directory to sys.path to allow absolute imports of sibling modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph import StudioLoopGraph
from state_store import StateStore
from role_loader import RoleLoader
from context_pruner import ContextPruner
from prompt_compiler import PromptCompiler
from kobold_client import KoboldClient
from artifact_validator import ArtifactValidator
from transition_engine import TransitionEngine
from command_runner import CommandRunner
from capability_registry import CapabilityRegistry
from response_parser import ResponseParser
from file_writer import FileWriter
from patch_applier import PatchApplier
from test_runner import TestRunner
from research_client import ResearchClient
from copyright_guard import CopyrightGuard
from safety_guard import SafetyGuard
from retry_engine import RetryEngine
from artifact_store import ArtifactStore
from source_indexer import SourceIndexer
from hooks import OrchestratorHooks
from context_compactor import ContextCompactor


class StudioLoopOrchestrator:
    def __init__(self, base_path):
        self.base_path = base_path
        self.config_path = os.path.join(base_path, ".agent/orchestrator/config.json")
        self.config = self.load_config()
        
        # Core Orchestration
        self.graph = StudioLoopGraph(os.path.join(base_path, self.config["paths"]["schema"]))
        self.state_store = StateStore(os.path.join(base_path, self.config["paths"]["state"]))
        self.role_loader = RoleLoader(base_path)
        self.pruner = ContextPruner(self.config)
        self.compiler = PromptCompiler(self.config)
        self.client = KoboldClient(self.config)
        self.transition_engine = TransitionEngine(self.graph)
        
        # Execution & Tooling
        self.command_runner = CommandRunner(base_path, ".agent/orchestrator/command_allowlist.json")
        self.file_writer = FileWriter(base_path)
        self.patch_applier = PatchApplier(base_path)
        self.test_runner = TestRunner(self.command_runner)
        self.compactor = ContextCompactor(base_path)
        self.hooks = OrchestratorHooks(base_path)
        
        # Wire up compaction and other hooks
        self.hooks.register_callback("after_transition", lambda ctx: self.compactor.compact(ctx["slug"], ctx["stage"], ctx["state"]))
        self.hooks.register_callback("before_write", lambda ctx: self.safety_guard.is_path_safe(ctx["path"], ctx["stage"]))
        self.hooks.register_callback("before_patch", lambda ctx: self.safety_guard.is_path_safe(ctx["path"], ctx["stage"]))

        self.research_client = ResearchClient(self.config)
        self.artifact_store = ArtifactStore(os.path.join(base_path, ".agent/Loop_Flow/"))
        self.source_indexer = SourceIndexer(base_path)
        
        # Guardrails & Parsers
        self.capability_registry = CapabilityRegistry(self.config)
        self.response_parser = ResponseParser(schema_path=os.path.join(self.base_path, ".agent/orchestrator/actions_schema.json"))
        self.copyright_guard = CopyrightGuard()
        self.safety_guard = SafetyGuard(base_path)
        self.retry_engine = RetryEngine(max_retries=self.config.get("automation", {}).get("max_stage_retries", 3))
        self.artifact_validator = ArtifactValidator(base_path)

    def load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def run(self, feature_text, mode="single_stage"):
        safe_feature = self.copyright_guard.transform_prompt(feature_text)
        print(f"Original request: {feature_text}")
        if safe_feature != feature_text:
            print(f"Transformed (copyright-safe): {safe_feature}")
            
        slug = self.pruner.generate_slug(safe_feature)
        start_stage = self.transition_engine.determine_initial_stage(safe_feature)
        state = self.state_store.start_feature(safe_feature, slug, start_stage)
        
        self.detect_capabilities()
        
        print(f"Starting feature: {safe_feature} (slug: {slug})")
        print(f"Initial stage: {start_stage}")
        
        if mode == "auto":
            self.autonomous_loop()
        else:
            self.execute_stage(start_stage)

    def autonomous_loop(self):
        state = self.state_store.load_state()
        stage_count = 0
        max_stages = self.config.get("automation", {}).get("max_total_stages", 20)
        
        while state["active"] and stage_count < max_stages:
            stage_count += 1
            current_stage = state["current_stage"]
            if current_stage == "handover_complete":
                print("Autonomous run complete: Terminal state reached.")
                break
                
            print(f"\n--- [Stage {stage_count}: {current_stage}] ---")
            success = self.execute_stage(current_stage)
            
            state = self.state_store.load_state()
            
            if not success or state["status"] == "blocked":
                print(f"Autonomous loop stopped at {current_stage} due to block or failure.")
                break
            
            if state["status"] == "failed" and not self.retry_stage(current_stage):
                print(f"Autonomous loop stopped: Max retries exceeded for {current_stage}.")
                break

    def execute_stage(self, stage_name, attempt=0, repair_prompt_override=None):
        state = self.state_store.load_state()
        if not state["active"]:
            print("No active feature. Run 'run <feature>' first.")
            return False

        print(f"Stage: {stage_name}")
        
        if repair_prompt_override:
            prompt = repair_prompt_override
        else:
            # 1. Build Context
            print("Building context...")
            source_context = self.source_indexer.generate_context_summary()
            pack_path = self.pruner.build_context_pack(state["feature_slug"], stage_name, state["feature"], state)
            with open(pack_path, 'r', encoding='utf-8') as f:
                context_content = f.read()
            
            # 2. Compile Prompt
            role_workflow = self.role_loader.load_role_workflow(stage_name)
            role_skills = self.role_loader.load_role_skills(stage_name)
            val_rules = self.graph.get_validation_rules(stage_name)
            req_outputs = self.graph.get_required_outputs(stage_name)
            
            prompt = self.compiler.compile_prompt(
                stage_name, state["feature"], state["feature"], state,
                role_workflow, role_skills, context_content + "\n" + source_context, 
                val_rules, req_outputs
            )
        
        # 3. Call Model
        print(f"Requesting actions from local model (attempt {attempt+1})...")
        self.hooks.trigger("before_model_call", {"stage": stage_name, "prompt": prompt})
        response_text = self.client.call(prompt)
        self.hooks.trigger("after_model_call", {"stage": stage_name, "response": response_text})
        
        # 4. Parse Response
        parsed = self.response_parser.parse(response_text)
        actions = parsed["actions"]
        
        # 5. Validate Actions
        is_valid, err = self.response_parser.validate_actions(actions)
        if not is_valid:
            print(f"Invalid ACTIONS_JSON: {err}")
            if self.retry_engine.should_retry(attempt):
                return self.repair_output(response_text, err, stage_name, attempt + 1)
            return False

        # 6. Safety Guard
        safe, err = self.safety_guard.validate_actions(stage_name, actions)
        if not safe:
            print(f"Safety Guard Blocked Actions: {err}")
            # We treat safety violations as failures that require repair
            if self.retry_engine.should_retry(attempt):
                return self.repair_output(response_text, f"SAFETY_VIOLATION: {err}", stage_name, attempt + 1)
            return False

        # 7. Execute Actions
        print("Executing actions...")
        execution_results, research_performed = self.perform_actions(stage_name, actions, parsed["writes"], parsed["patches"])
        
        # 7. Two-Pass Research Re-entry
        if research_performed:
            # Check if research was blocked or failed fundamentally
            any_blocked = any(r.get("status") == "blocked" for r in execution_results["research"])
            if any_blocked:
                print("Research blocked. Transitioning to failure state or retrying with human help.")
                # If research is required but blocked, we cannot proceed normally
                val_rules = self.graph.get_validation_rules(stage_name)
                if val_rules.get("research_required"):
                    print("Mandatory research blocked. Marking stage as failed.")
                    return False
            
            print("Research performed. Re-entering stage with updated context...")
            # We don't increment attempt for research re-entry
            return self.execute_stage(stage_name, attempt)

        # 8. Post-Execution Validation
        if actions.get("status") == "complete":
            # Post-Execution Validation
            self.hooks.trigger("before_validation", {"stage": stage_name, "actions": actions})
            val_report = self.validate_stage(stage_name, actions, execution_results)
            self.hooks.trigger("after_validation", {"stage": stage_name, "report": val_report})
            if not val_report["valid"]:
                print(f"Stage validation failed: {val_report['errors']}")
                if self.retry_engine.should_retry(attempt):
                    return self.execute_stage(stage_name, attempt + 1)
                return False
            
            # 8. Success & Transition
            print(f"Stage {stage_name} complete and validated.")
            self.state_store.complete_stage(stage_name, {"actions": actions, "results": execution_results})
            
            next_stage = self.transition_engine.get_next_stage(stage_name, actions, val_report)
            self.state_store.set_current_stage(next_stage)
            
            # Trigger hook
            self.hooks.trigger("after_transition", {
                "slug": state.get("feature_slug"),
                "stage": stage_name,
                "state": state,
                "next_stage": next_stage
            })
            
            return True

            
        return False

    def perform_actions(self, stage, actions, extra_writes, extra_patches):
        state = self.state_store.load_state()
        feature_slug = state.get("feature_slug")
        results = {"writes": [], "patches": [], "commands": [], "research": []}
        
        # 1. Research
        for req in actions.get("research_requests", []):
            self.hooks.trigger("before_research", {"stage": stage, "query": req["query"]})
            res = self.research_client.perform_research(req["query"], req.get("reason"), feature_slug=feature_slug, stage=stage)
            results["research"].append(res)
            
            # Record in state
            if res.get("artifact_path"):
                if "research_briefs" not in state:
                    state["research_briefs"] = []
                if "research_results" not in state:
                    state["research_results"] = []
                state["research_briefs"].append(res["artifact_path"])
                state["research_results"].append(res)
                self.hooks.trigger("after_research", {"stage": stage, "query": req["query"], "results": res})
                self.state_store.save_state(state)

        # 2. Writes
        all_writes = actions.get("writes", []) + extra_writes
        for w in all_writes:
            self.hooks.trigger("before_write", {"stage": stage, "path": w["path"]})
            success, err = self.file_writer.write(stage, w["path"], w["content"], w.get("mode", "overwrite"))
            self.hooks.trigger("after_write", {"stage": stage, "path": w["path"], "success": success})
            results["writes"].append({"path": w["path"], "success": success, "error": err})

        # 3. Patches
        all_patches = actions.get("patches", []) + extra_patches
        for p in all_patches:
            self.hooks.trigger("before_patch", {"stage": stage, "path": p["path"]})
            success, err = self.patch_applier.apply(stage, p["path"], p["diff"])
            self.hooks.trigger("after_patch", {"stage": stage, "path": p["path"], "success": success})
            results["patches"].append({"path": p["path"], "success": success, "error": err})

        # 4. Commands
        for cmd in actions.get("commands", []):
            self.hooks.trigger("before_command", {"stage": stage, "command": cmd})
            res = self.command_runner.run(cmd["name"], cmd.get("args"))
            self.hooks.trigger("after_command", {"stage": stage, "result": res})
            results["commands"].append(res)
            
        research_performed = len(results["research"]) > 0
        return results, research_performed

    def validate_stage(self, stage_name, actions, results):
        state = self.state_store.load_state()
        val_rules = self.graph.get_validation_rules(stage_name)
        
        # 1. Structural & File Validation
        report = self.artifact_validator.validate(stage_name, actions, results, val_rules, state)
        errors = report["errors"]
        
        # 2. Copyright Scan
        summary_violations = self.copyright_guard.scan_text(actions.get("summary", ""))
        for v in summary_violations:
            errors.append(f"Copyright violation in summary: {v['term']}")
            
        # 3. Content Scan (Writes)
        for w in results.get("writes", []):
            if w["success"]:
                try:
                    with open(os.path.join(self.base_path, w["path"]), 'r', encoding='utf-8') as f:
                        content = f.read()
                    violations = self.copyright_guard.scan_text(content, is_research=(stage_name == "researcher"))
                    for v in violations:
                        errors.append(f"Copyright violation in file {w['path']}: {v['term']}")
                except Exception:
                    pass

        # 4. Content Scan (Patches)
        for p in results.get("patches", []):
            if p["success"]:
                try:
                    with open(os.path.join(self.base_path, p["path"]), 'r', encoding='utf-8') as f:
                        content = f.read()
                    violations = self.copyright_guard.scan_text(content)
                    for v in violations:
                        errors.append(f"Copyright violation in patched file {p['path']}: {v['term']}")
                except Exception:
                    pass

        # 5. Typecheck & Quality
        changed_paths = [w["path"] for w in results.get("writes", []) if w["success"]] + \
                        [p["path"] for p in results.get("patches", []) if p["success"]]
        
        source_extensions = ('.ts', '.tsx', '.js', '.jsx', '.json', '.py', '.css')
        source_dirs = ('src/', 'tests/', 'tools/', 'data/')
        
        is_source_change = any(
            p.endswith(source_extensions) or any(p.startswith(sd) for sd in source_dirs)
            for p in changed_paths
        )
        
        if is_source_change:
            print("Source change detected. Running quality checks...")
            suite = self.test_runner.run_full_suite()
            
            # Store results in state for context
            state["last_quality_check"] = suite
            self.state_store.save_state(state)
            
            if not suite["typecheck"].get("success"):
                errors.append("Typecheck failed after changes.")
            if not suite["tests"].get("success"):
                # Only fail if tests exist and failed
                if "No tests found" not in suite["tests"].get("stdout", ""):
                    errors.append("Unit tests failed after changes.")
            if not suite["bloat"].get("success"):
                errors.append("Bloat check failed: oversized files detected.")
                
        # Write validation report to log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.base_path, f".agent/logs/validation/{timestamp}_{state['feature_slug']}_{stage_name}.json")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({"valid": len(errors) == 0, "errors": errors, "actions": actions, "results": results}, f, indent=2)

        return {"valid": len(errors) == 0, "errors": errors}

    def detect_capabilities(self):
        caps = self.capability_registry.detect_all()
        self.state_store.update_capabilities(caps)
        print("Capabilities detected and stored.")

    def repair_output(self, raw_response, error, stage_name, attempt):
        print(f"Attempting output repair (attempt {attempt})...")
        
        # 1. Generate repair prompt
        error_type = "SCHEMA_ERROR" if "JSON" in error else "VALIDATION_FAILED"
        repair_prompt = self.retry_engine.get_repair_prompt(error_type, error, context_snippet=raw_response[:1000])
        
        # 2. Get repair response from model
        # For now, we simulate the model call via execute_stage but passing the repair prompt
        # In a real implementation, execute_stage would take an optional override_prompt
        return self.execute_stage(stage_name, attempt, repair_prompt_override=repair_prompt)

    def status(self):
        state = self.state_store.load_state()
        print(json.dumps(state, indent=2))

    def reset(self):
        self.state_store.reset_state()
        
        # Cleanup all generated artifacts and logs
        import shutil
        cleanup_dirs = [
            ".agent/Loop_Flow",
            ".agent/Loop_Flow/context_packs",
            ".agent/Loop_Flow/research",
            ".agent/logs"
        ]
        
        for d in cleanup_dirs:
            full_dir = os.path.join(self.base_path, d)
            if not os.path.exists(full_dir):
                continue
                
            for item in os.listdir(full_dir):
                item_path = os.path.join(full_dir, item)
                if item == ".gitkeep":
                    continue
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        # For subdirectories like .agent/logs/validation, we want to clean them too
                        # but keep their .gitkeep if they have one? 
                        # Actually, instruction says clean everything but .gitkeep.
                        # If it's a directory, we can rmtree but we might lose .gitkeep inside.
                        # Let's be surgical.
                        self._surgical_dir_clean(item_path)
                except Exception as e:
                    print(f"Error cleaning {item_path}: {e}")
        
        # Also clean any test_final.txt in root
        if os.path.exists(os.path.join(self.base_path, "test_final.txt")):
            os.remove(os.path.join(self.base_path, "test_final.txt"))
                
        print("State, artifacts, and logs reset.")

    def _surgical_dir_clean(self, dir_path):
        import shutil
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if item == ".gitkeep":
                continue
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                self._surgical_dir_clean(item_path)
                # If directory is now empty (except maybe .gitkeep), we could remove it, 
                # but standard practice is often to keep the structure.
                # The instruction says remove generated artifacts.
                if not os.listdir(item_path) or (len(os.listdir(item_path)) == 1 and os.listdir(item_path)[0] == ".gitkeep"):
                    pass # keep it
                else:
                    shutil.rmtree(item_path)

    def retry_stage(self, stage_name):
        return self.execute_stage(stage_name, attempt=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Studio Loop Orchestrator 4.0")
    parser.add_argument("command", choices=["run", "auto", "continue", "step", "retry", "repair", "status", "reset", "validate", "context", "research", "capabilities"])
    parser.add_argument("payload", nargs="?", help="Task description or query")
    
    args = parser.parse_args()
    base_dir = os.getcwd()
    orchestrator = StudioLoopOrchestrator(base_dir)
    
    state = orchestrator.state_store.load_state()

    if args.command == "run":
        orchestrator.run(args.payload or "New task", mode="single_stage")
    elif args.command == "auto":
        orchestrator.run(args.payload or "New task", mode="auto")
    elif args.command == "continue":
        if state["active"]:
            orchestrator.autonomous_loop()
        else:
            print("No active feature to continue.")
    elif args.command == "step":
        if state["active"]:
            orchestrator.execute_stage(state["current_stage"])
        else:
            print("No active feature to step.")
    elif args.command == "retry":
        if state["active"]:
            orchestrator.retry_stage(state["current_stage"])
        else:
            print("No active feature to retry.")
    elif args.command == "repair":
        if state["active"]:
            orchestrator.repair_output("", "Manual repair request", state["current_stage"], 0)
        else:
            print("No active feature to repair.")
    elif args.command == "status":
        orchestrator.status()
    elif args.command == "reset":
        orchestrator.reset()
    elif args.command == "validate":
        if state["active"]:
            res = orchestrator.validate_stage(state["current_stage"], state.get("last_actions", {}), {"writes": [], "patches": []})
            print(json.dumps(res, indent=2))
        else:
            print("No active feature to validate.")
    elif args.command == "context":
        if state["active"]:
            source_context = orchestrator.source_indexer.generate_context_summary()
            pack_path = orchestrator.pruner.build_context_pack(state["feature_slug"], state["current_stage"], state["feature"], state)
            print(f"Context pack: {pack_path}")
            print(source_context[:1000] + "...")
        else:
            print("No active feature for context.")
    elif args.command == "research":
        if args.payload:
            res = orchestrator.research_client.perform_research(args.payload)
            print(json.dumps(res, indent=2))
        else:
            print("Research requires a query payload.")
    elif args.command == "capabilities":
        orchestrator.detect_capabilities()
        print(json.dumps(orchestrator.state_store.load_state()["capabilities"], indent=2))
