import os
from skill_registry import SkillRegistry

class RoleLoader:
    ROLE_MAPPING = {
        "concept_producer": ".agent/workflows/concept_producer.md",
        "researcher": ".agent/workflows/researcher.md",
        "designer": ".agent/workflows/designer.md",
        "developer": ".agent/workflows/developer.md",
        "qa_tester": ".agent/workflows/qa_tester.md",
        "bug_hunter": ".agent/workflows/bug_hunter.md",
        "debug_dev": ".agent/workflows/debug_dev.md",
        "asset_creator": ".agent/workflows/asset_creator.md"
    }

    SKILL_MAPPING = {
        "concept_producer": ["producer_skills.md"],
        "researcher": ["researcher_skills.md"],
        "designer": ["designer_skills.md"],
        "developer": ["developer_skills.md"],
        "qa_tester": ["qa_skills.md"],
        "asset_creator": ["asset_creator_skills.md"],
        "bug_hunter": ["qa_skills.md", "researcher_skills.md"],
        "debug_dev": ["developer_skills.md"]
    }

    def __init__(self, base_path):
        self.base_path = base_path
        self.skill_registry = SkillRegistry(base_path)

    def load_role_workflow(self, role_name):
        rel_path = self.ROLE_MAPPING.get(role_name)
        if not rel_path:
            raise ValueError(f"Unknown role: {role_name}")
        
        full_path = os.path.join(self.base_path, rel_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Workflow file not found: {full_path}")
            
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_role_skills(self, role_name):
        manifests = self.load_role_skill_manifests(role_name)
        if manifests:
            skills_content = []
            for manifest in manifests:
                summary = self.skill_registry.summarize_manifest(manifest)
                markdown = self.skill_registry.load_skill_markdown(manifest)
                skills_content.append(
                    f"### Skill: {manifest['id']}@{manifest['version']}\n"
                    f"Manifest:\n```json\n{summary}\n```\n\n{markdown}"
                )
            return "\n\n".join(skills_content)

        skill_files = self.SKILL_MAPPING.get(role_name, [])
        skills_content = []
        
        for sf in skill_files:
            full_path = os.path.join(self.base_path, ".agent/skills", sf)
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    skills_content.append(f"### Skill: {sf}\n{f.read()}")
            else:
                skills_content.append(f"### Skill: {sf} (Not Found)")
        
        return "\n\n".join(skills_content)

    def load_role_skill_manifests(self, role_name):
        try:
            return self.skill_registry.get_role_skills(role_name)
        except FileNotFoundError:
            return []
