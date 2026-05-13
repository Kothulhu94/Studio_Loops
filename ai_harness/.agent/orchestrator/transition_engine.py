class TransitionEngine:
    def __init__(self, graph):
        self.graph = graph

    def determine_initial_stage(self, user_request):
        request = user_request.lower()
        if any(word in request for word in ["bug", "fix", "broken", "error"]):
            return "bug_hunter"
        if any(word in request for word in ["ui", "look", "design", "aesthetic"]):
            return "concept_producer"
        if any(word in request for word in ["research", "how to", "architecture"]):
            return "field_researcher"
        return "concept_producer"

    def get_next_stage(self, current_stage, actions, validation_result):
        if not validation_result.get("valid", True):
            return current_stage # Stay and retry

        status = actions.get("status")
        if status == "blocked" or status == "failed":
            return current_stage

        # Check for explicit recommendation from model
        rec = actions.get("next_stage_recommendation")
        allowed_next = self.graph.get_allowed_next(current_stage)
        if current_stage == "researcher" and rec == "designer" and not actions.get("design_required", False):
            return "developer"
        if rec and rec in allowed_next:
            return rec

        # Transition Rules
        if current_stage == "concept_producer":
            return "field_researcher"
        
        elif current_stage == "field_researcher":
            return "lab_assistant"
            
        elif current_stage == "lab_assistant":
            if actions.get("design_required"):
                return "designer"
            return "developer"
        
        elif current_stage == "researcher":
            if actions.get("design_required"):
                return "designer"
            return "developer"
        
        elif current_stage == "designer":
            if actions.get("assets_required"):
                return "asset_creator"
            return "developer"
        
        elif current_stage == "asset_creator":
            return "developer"
        
        elif current_stage == "developer":
            return "qa_tester"
        
        elif current_stage == "qa_tester":
            qa_res = actions.get("qa_result")
            if qa_res == "PASS":
                return "handover_complete"
            elif qa_res == "FAIL":
                return "bug_hunter"
            elif qa_res == "BLOCKED":
                return current_stage
            elif qa_res == "SKIPPED" and not actions.get("blockers"):
                return "handover_complete"
            return current_stage # Stay if ambiguous
        
        elif current_stage == "bug_hunter":
            return "debug_dev"
        
        elif current_stage == "debug_dev":
            return "qa_tester"

        return "handover_complete"
