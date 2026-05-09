import json
import os

class StudioLoopGraph:
    def __init__(self, schema_path):
        self.schema_path = schema_path
        self.schema = self.load_schema()

    def load_schema(self):
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema not found at {self.schema_path}")
        with open(self.schema_path, 'r') as f:
            return json.load(f)

    def get_stage(self, stage_name):
        return self.schema.get("stages", {}).get(stage_name)

    def get_next_stages(self, stage_name):
        stage = self.get_stage(stage_name)
        return stage.get("next_stages", []) if stage else []

    def get_required_inputs(self, stage_name):
        stage = self.get_stage(stage_name)
        return stage.get("required_input", []) if stage else []

    def get_required_outputs(self, stage_name):
        stage = self.get_stage(stage_name)
        return stage.get("required_output", []) if stage else []

    def get_validation_rules(self, stage_name):
        stage = self.get_stage(stage_name)
        return stage.get("validation", {}) if stage else {}

    def is_valid_transition(self, from_stage, to_stage):
        if from_stage is None:
            return to_stage in self.schema.get("stages", {})
        allowed = self.get_allowed_next(from_stage)
        return to_stage in allowed

    def get_allowed_next(self, stage_name):
        next_stages = self.get_next_stages(stage_name)
        return next_stages + ["handover_complete"]
