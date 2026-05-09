import json
import os

class RetryEngine:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def get_repair_prompt(self, error_type, error_message, context_snippet=None):
        """Generates a targeted repair prompt as per Section 18."""
        prompt = f"### REPAIR REQUEST: {error_type}\n\n"
        prompt += f"The orchestrator rejected the previous action due to the following error:\n\n"
        prompt += f"ERROR:\n{error_message}\n\n"
        
        if context_snippet:
            prompt += f"RELEVANT CONTEXT:\n{context_snippet}\n\n"
            
        prompt += "INSTRUCTION:\n"
        prompt += "1. Identify the cause of the failure.\n"
        prompt += "2. Return a corrected ACTIONS_JSON block only.\n"
        prompt += "3. Do not repeat failed patches or writes without modification.\n"
        prompt += "4. If this was a JSON syntax error, ensure the new JSON is valid and escaped correctly.\n"
        
        return prompt

    def should_retry(self, attempt_count):
        return attempt_count < self.max_retries

    def update_state_attempts(self, state, stage):
        attempts = state.get("stage_attempts", {})
        attempts[stage] = attempts.get(stage, 0) + 1
        state["stage_attempts"] = attempts
        return state
