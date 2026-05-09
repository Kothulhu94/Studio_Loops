import json
import os

class RetryEngine:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def get_repair_prompt(self, error_type, error_message, context_snippet=None, stage_name=None):
        """Generates a targeted repair prompt as per Section 18."""
        prompt = f"### REPAIR REQUEST: {error_type}\n\n"
        if stage_name:
            prompt += f"CURRENT STAGE:\n{stage_name}\n\n"
        prompt += f"The orchestrator rejected the previous action due to the following error:\n\n"
        prompt += f"ERROR:\n{error_message}\n\n"
        
        if context_snippet:
            prompt += f"PREVIOUS RESPONSE EXCERPT:\n{context_snippet}\n\n"
            
        prompt += "INSTRUCTION:\n"
        prompt += "1. Return exactly one ACTIONS_JSON block.\n"
        prompt += "2. Do not include prose before or after.\n"
        prompt += "3. Use valid JSON.\n"
        prompt += "4. Use null as JSON null, not \"null\".\n"
        prompt += "5. Do not invent writes/patches unless needed to satisfy the original stage.\n"
        prompt += "6. The status field must be exactly one of: complete, blocked, failed. Replace invalid values such as running, in_progress, or pending.\n"
        prompt += "7. Do not wrap JSON in Markdown fences.\n"
        prompt += "8. Do not rename fields. Use next_stage_recommendation, not next_stage.\n"
        prompt += "9. If this was a JSON syntax error, ensure the new JSON is valid and escaped correctly.\n"
        
        return prompt

    def should_retry(self, attempt_count):
        return attempt_count < self.max_retries

    def update_state_attempts(self, state, stage):
        attempts = state.get("stage_attempts", {})
        attempts[stage] = attempts.get(stage, 0) + 1
        state["stage_attempts"] = attempts
        return state
