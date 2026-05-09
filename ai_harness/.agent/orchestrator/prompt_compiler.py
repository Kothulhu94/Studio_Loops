import json
import os

class PromptCompiler:
    def __init__(self, config):
        self.config = config
        self.template_path = os.path.join(
            os.path.dirname(__file__), 
            "templates", 
            "stage_prompt.md"
        )

    def compile_prompt(self, stage, feature, user_request, state, role_workflow, role_skills, context_pack_content, validation_rules, required_outputs):
        if os.path.exists(self.template_path):
            from string import Template
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_str = f.read()
            
            template = Template(template_str)
            user_prompt = template.safe_substitute(
                stage=stage,
                feature=feature,
                user_request=user_request,
                state=json.dumps(state, indent=2),
                role_instructions=role_workflow,
                skills=role_skills,
                artifacts=".agent/Loop_Flow/", 
                context=context_pack_content,
                required_outputs=json.dumps(required_outputs, indent=2),
                validation_rules=json.dumps(validation_rules, indent=2)
            )
        else:
            # Fallback (updated to remove forbidden terms)
            user_prompt = f"# Studio Loop Stage Prompt\nRole: {stage}\nFeature: {feature}"

        system_prompt = (
            f"You are the active Studio Loop role: {stage}.\n"
            "The orchestrator controls transitions.\n"
            "Do not include hidden reasoning.\n"
            "Complete only the current stage.\n"
        )

        return {
            "system": system_prompt,
            "user": user_prompt
        }
