import json
import os

class RetryEngine:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def get_repair_prompt(self, error_type, error_message, context_snippet=None, stage_name=None, results=None, stack_profile="game_source"):
        """Generates a targeted repair prompt as per Section 18."""
        current_stage = stage_name or "<current_stage>"
        prompt = f"### REPAIR REQUEST: {error_type}\n\n"
        if stage_name:
            prompt += f"CURRENT STAGE:\n{stage_name}\n\n"
        prompt += "GEMMA 4 REPAIR MODE:\n"
        prompt += "- Treat this as a logical debugging task. Analyze WHY the previous code failed.\n"
        prompt += "- Think silently. Identify if you are missing a definition or an import.\n"
        prompt += "- If you are missing a definition (e.g. 'Cannot find name'), you MUST request research (file_reader) to find it before marking complete.\n"
        prompt += "- Output only the corrected ACTIONS_JSON block.\n"
        prompt += "- Do not use placeholders like /* dependencies */ or // fix later. Write functional code.\n\n"
        prompt += f"The orchestrator rejected the previous action due to the following error:\n\n"
        prompt += f"ERROR:\n{error_message}\n\n"
        
        if context_snippet:
            prompt += f"OFFENDING CODE SNIPPET:\n{context_snippet}\n\n"

        if "RESEARCH_REQUIRED_MISSING" in error_message:
            prompt += "REQUIRED RESEARCH REPAIR:\n"
            prompt += "- This stage has research_required=true.\n"
            prompt += "- Return status blocked with one or more research_requests.\n"
            prompt += "- Do not write the final technical blueprint until research has completed.\n"
            prompt += "- Do not include writes or patches in this repair response.\n"
            if stack_profile == "harness_internal":
                prompt += "- For harness_internal: use Python for orchestrator/tooling changes; use tests/*.py and tools/verify_clean_runtime.py for verification.\n\n"
                prompt += "- If exact local paths are unknown, request mode=\"local_codebase\" with audit_kind=\"discovery\" and target_files [\".agent\", \"tests\", \"tools\"] instead of guessing paths.\n\n"
            else:
                prompt += "- Use TypeScript/browser/Vitest stack research only.\n\n"
        
        if results:
            prompt += "ACTION EXECUTION STATUS:\n"
            # Limit results to avoid context blowup but keep errors
            if isinstance(results, dict):
                compact_results = {k: v for k, v in results.items() if k != "execution_results"}
                prompt += json.dumps(compact_results, indent=2)[:2000] + "\n"
            
            if results.get("write_results"):
                prompt += "Last Writes:\n"
                for w in results["write_results"]:
                    status = "SUCCESS" if w["success"] else f"FAILED: {w['error']}"
                    prompt += f"- {w['path']}: {status}\n"
            
            if results.get("quality_check"):
                qc = results["quality_check"]
                prompt += "QUALITY CHECK STATUS:\n"
                if "typecheck" in qc:
                    t = qc["typecheck"]
                    t_status = "PASSED" if t["success"] else "FAILED"
                    prompt += f"- Typecheck: {t_status}\n"
                    if not t["success"]:
                        prompt += f"  Errors:\n{t['stderr'] or t['stdout']}\n"
            prompt += "\n"

        if "POST_EXECUTION_VALIDATION_FAILED" in error_message:
            prompt += "POST-VALIDATION REPAIR:\n"
            prompt += "- If you can fix the validation error by writing missing or corrected artifacts, return status complete.\n"
            prompt += "- If you encounter a missing definition error, do not guess; use research_requests to read the source file first.\n\n"

        prompt += "INSTRUCTION:\n"
        prompt += "1. Return exactly one ACTIONS_JSON block.\n"
        prompt += "2. Include a 'reasoning' field explaining how you addressed the specific error above.\n"
        prompt += "3. Use valid JSON.\n"
        prompt += "4. If a file already exists and you intended to update it, use mode=\"overwrite\".\n"
        prompt += "5. Do not use placeholders. If you don't know a type or value, request research.\n"
        prompt += "6. The status field must be exactly one of: complete, blocked, failed.\n"
        prompt += "7. Do not wrap JSON in Markdown fences.\n"
        prompt += "8. Ensure research_required is satisfied if true in the validation rules.\n"
        
        if stack_profile == "harness_internal":
            prompt += "9. For harness_internal: use Python for orchestrator/tooling changes.\n"
        else:
            prompt += "9. For game_source: use TypeScript/browser/Vitest.\n"
            
        prompt += "10. Include stage, status, reasoning, and summary.\n\n"
        prompt += "REQUIRED ROOT SHAPE:\n"
        prompt += "ACTIONS_JSON:\n"
        root_status = "complete" if "POST_EXECUTION_VALIDATION_FAILED" in error_message else "blocked"
        prompt += json.dumps({
            "stage": current_stage,
            "status": root_status,
            "reasoning": "Explain your debugging steps here.",
            "summary": "Brief summary of the fix.",
            "research_requests": [],
            "writes": [],
            "patches": [],
            "commands": [],
            "next_stage_recommendation": None
        }, indent=2)
        prompt += "\n"
        
        return prompt

    def should_retry(self, attempt_count):
        return attempt_count < self.max_retries

    def update_state_attempts(self, state, stage):
        attempts = state.get("stage_attempts", {})
        attempts[stage] = attempts.get(stage, 0) + 1
        state["stage_attempts"] = attempts
        return state
