import json
import os


class SkillRegistry:
    TRUSTED_LEVELS = {"core", "local"}
    REQUIRED_FIELDS = {
        "id",
        "name",
        "version",
        "roles",
        "required_tools",
        "allowed_write_paths",
        "expected_artifacts",
        "validators",
        "provenance",
        "trust_level",
    }

    def __init__(self, base_path, registry_path=".agent/skills/registry.json", allow_external=False):
        self.base_path = base_path
        self.registry_path = os.path.join(base_path, registry_path)
        self.allow_external = allow_external
        self._skills = None

    def load(self):
        if self._skills is not None:
            return self._skills
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(f"Skill registry not found: {self.registry_path}")
        with open(self.registry_path, "r", encoding="utf-8") as handle:
            registry = json.load(handle)
        skills = {}
        for entry in registry.get("skills", []):
            manifest_path = os.path.join(self.base_path, entry["manifest"])
            manifest = self.load_manifest(manifest_path)
            trust_level = manifest.get("trust_level")
            if trust_level not in self.TRUSTED_LEVELS and not self.allow_external:
                continue
            skills[manifest["id"]] = manifest
        self._skills = skills
        return skills

    def load_manifest(self, manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        missing = sorted(self.REQUIRED_FIELDS - set(manifest.keys()))
        if missing:
            raise ValueError(f"Skill manifest missing fields {missing}: {manifest_path}")
        trust_level = manifest.get("trust_level")
        if trust_level not in {"core", "local", "external"}:
            raise ValueError(f"Invalid trust_level '{trust_level}' in {manifest_path}")
        manifest["_manifest_path"] = os.path.relpath(manifest_path, self.base_path).replace("\\", "/")
        manifest["_skill_dir"] = os.path.dirname(manifest_path)
        return manifest

    def get_role_skills(self, role_name):
        skills = []
        for manifest in self.load().values():
            if role_name in manifest.get("roles", []):
                skills.append(manifest)
        return sorted(skills, key=lambda item: item["id"])

    def load_skill_markdown(self, manifest):
        skill_dir = manifest.get("_skill_dir")
        skill_path = os.path.join(skill_dir, "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path, "r", encoding="utf-8") as handle:
                content = handle.read()
            legacy_path = manifest.get("legacy_markdown")
            if legacy_path:
                with open(os.path.join(self.base_path, legacy_path), "r", encoding="utf-8") as handle:
                    content = content.rstrip() + "\n\n" + handle.read()
        else:
            legacy_path = manifest.get("legacy_markdown")
            if not legacy_path:
                content = ""
            else:
                with open(os.path.join(self.base_path, legacy_path), "r", encoding="utf-8") as handle:
                    content = handle.read()
        return content

    def summarize_manifest(self, manifest):
        public_fields = {
            "id": manifest["id"],
            "version": manifest["version"],
            "roles": manifest["roles"],
            "required_tools": manifest["required_tools"],
            "allowed_write_paths": manifest["allowed_write_paths"],
            "expected_artifacts": manifest["expected_artifacts"],
            "validators": manifest["validators"],
            "provenance": manifest["provenance"],
            "trust_level": manifest["trust_level"],
        }
        return json.dumps(public_fields, indent=2)

    def allowed_write_paths_for_role(self, role_name):
        allowed = []
        for manifest in self.get_role_skills(role_name):
            allowed.extend(manifest.get("allowed_write_paths", []))
        return sorted(set(allowed))

    def expected_artifacts_for_role(self, role_name):
        artifacts = []
        for manifest in self.get_role_skills(role_name):
            artifacts.extend(manifest.get("expected_artifacts", []))
        return artifacts

    def validators_for_role(self, role_name):
        validators = []
        for manifest in self.get_role_skills(role_name):
            validators.extend(manifest.get("validators", []))
        return sorted(set(validators))
