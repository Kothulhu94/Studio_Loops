import json
import os

class RetryEngine:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def get_repair_prompt(self, error_type, error_message, context_snippet=None, stage_name=None, results=None):
        """Generates a targeted repair prompt as per Section 18."""
        prompt = f"### REPAIR REQUEST: {error_type}\n\n"
        if stage_name:
            prompt += f"CURRENT STAGE:\n{stage_name}\n\n"
        prompt += f"The orchestrator rejected the previous action due to the following error:\n\n"
        prompt += f"ERROR:\n{error_message}\n\n"
        if "RESEARCH_REQUIRED_MISSING" in error_message:
            prompt += "REQUIRED RESEARCH REPAIR:\n"
            prompt += "- This stage has research_required=true.\n"
            prompt += "- Return status blocked with one or more research_requests.\n"
            prompt += "- Do not write the final technical blueprint until research has completed.\n"
            prompt += "- Do not include writes or patches in this repair response.\n"
            prompt += "- Use TypeScript/browser/Vitest stack research only.\n\n"
        
        if results:
            prompt += "ACTION EXECUTION STATUS:\n"
            prompt += json.dumps(results, indent=2)[:4000] + "\n"
            if results.get("writes"):
                prompt += "Writes:\n"
                for w in results["writes"]:
                    status = "SUCCESS" if w["success"] else f"FAILED: {w['error']}"
                    prompt += f"- {w['path']}: {status}\n"
            if results.get("patches"):
                prompt += "Patches:\n"
                for p in results["patches"]:
                    status = "SUCCESS" if p["success"] else f"FAILED: {p['error']}"
                    prompt += f"- {p['path']}: {status}\n"
            prompt += "\n"

        if context_snippet:
            prompt += f"PREVIOUS RESPONSE EXCERPT:\n{context_snippet}\n\n"
            
        prompt += "INSTRUCTION:\n"
        prompt += "1. Return exactly one ACTIONS_JSON block.\n"
        prompt += "2. Do not include prose before or after.\n"
        prompt += "3. Use valid JSON.\n"
        prompt += "4. Use null as JSON null, not \"null\".\n"
        prompt += "5. If a file already exists and you intended to update it, use mode=\"overwrite\".\n"
        prompt += "6. Do not use mode=\"create\" for files that already exist according to the status above.\n"
        prompt += "7. Do not invent writes/patches unless needed to satisfy the original stage.\n"
        prompt += "8. The status field must be exactly one of: complete, blocked, failed. Replace invalid values such as running, in_progress, or pending.\n"
        prompt += "9. Do not wrap JSON in Markdown fences.\n"
        prompt += "10. Do not rename fields. Use next_stage_recommendation, not next_stage.\n"
        prompt += "11. Ensure research_required is satisfied if true in the validation rules.\n"
        prompt += "12. If research is required and no complete research exists, request research first and do not write a final technical blueprint yet.\n"
        prompt += "13. For this project, use the TypeScript/browser/Vitest stack only; do not propose Python game source implementation.\n"
        
        return prompt

    def should_retry(self, attempt_count):
        return attempt_count < self.max_retries

    def update_state_attempts(self, state, stage):
        attempts = state.get("stage_attempts", {})
        attempts[stage] = attempts.get(stage, 0) + 1
        state["stage_attempts"] = attempts
        return state
