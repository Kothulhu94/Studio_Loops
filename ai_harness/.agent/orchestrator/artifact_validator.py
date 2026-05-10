import json
import os
import re

class ArtifactValidator:
    def __init__(self, base_path):
        self.base_path = base_path

    def validate_research_result(self, result):
        errors = []
        if result.get("status") != "complete":
            errors.append(f"Research status is not complete: {result.get('status')}")

        fetched_relevant_sources = [
            source for source in result.get("sources", [])
            if source.get("status") == "fetched"
            and source.get("relevant", True)
            and not source.get("rejected", False)
        ]
        if len(fetched_relevant_sources) < 2:
            errors.append("Research has fewer than 2 fetched relevant sources.")
        if len(result.get("findings", [])) < 2:
            errors.append("Research has fewer than 2 findings.")

        artifact_path = result.get("artifact_path")
        if not artifact_path:
            errors.append("Research has no artifact_path.")
        else:
            full_artifact_path = artifact_path
            if not os.path.isabs(full_artifact_path):
                full_artifact_path = os.path.join(self.base_path, full_artifact_path)
            if not os.path.exists(full_artifact_path):
                errors.append(f"Research artifact_path does not exist: {artifact_path}")

        if result.get("source_set_relevance_passed") is not True:
            errors.append("Research source-set relevance validation failed.")

        return errors

    def validate(self, stage, actions, execution_results, validation_rules, state, skill_manifests=None):
        errors = []
        warnings = []
        skill_manifests = skill_manifests or []

        if not actions:
            errors.append("Missing ACTIONS_JSON.")
            return {"valid": False, "errors": errors, "warnings": warnings}

        # 1. Validate stage matches
        if actions.get("stage") != stage:
            errors.append(f"Action stage mismatch: expected {stage}, got {actions.get('stage')}")

        # 2. Validate status
        if actions.get("status") not in ["complete", "blocked", "failed"]:
            errors.append(f"Invalid status in ACTIONS_JSON: {actions.get('status')}")

        # 3. Check required files and sections
        feature_slug = state.get("feature_slug", "")
        for req_file in validation_rules.get("required_files", []):
            req_file_processed = req_file.replace("{feature}", feature_slug)
            required_sections = validation_rules.get("required_sections", [])
            full_path = self._find_satisfying_artifact(
                req_file_processed,
                required_sections,
                actions,
                execution_results,
            )
            if not full_path:
                errors.append(f"Required file missing: {req_file_processed}")
                continue

            section_errors = self._validate_sections(full_path, required_sections, req_file_processed, "Required section")
            errors.extend(section_errors)

        for manifest in skill_manifests:
            for artifact in manifest.get("expected_artifacts", []):
                path_template = artifact.get("path")
                if not path_template:
                    continue
                artifact_path = path_template.replace("{feature}", feature_slug)
                required_sections = artifact.get("required_sections", [])
                full_path = self._find_satisfying_artifact(
                    artifact_path,
                    required_sections,
                    actions,
                    execution_results,
                )
                if not full_path:
                    if artifact.get("required", True):
                        errors.append(f"Expected skill artifact missing for {manifest['id']}: {artifact_path}")
                    continue
                section_errors = self._validate_sections(
                    full_path,
                    required_sections,
                    artifact_path,
                    "Expected skill artifact section",
                )
                errors.extend(section_errors)

        # 4. Check writes/patches (Safety & Line Limits)
        for w in execution_results.get("writes", []):
            if not w["success"]:
                errors.append(f"Write failed for {w['path']}: {w.get('error')}")
            else:
                # 500-line limit for source files
                if w["path"].endswith((".py", ".ts", ".js", ".tsx", ".jsx", ".css")):
                    try:
                        with open(os.path.join(self.base_path, w['path']), "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            if len(lines) > 500:
                                errors.append(f"File {w['path']} exceeds 500-line limit ({len(lines)} lines). Refactor needed.")
                    except Exception:
                        pass

        for p in execution_results.get("patches", []):
            if not p["success"]:
                errors.append(f"Patch failed for {p['path']}: {p.get('error')}")

        # 5. Check commands success
        for cmd in execution_results.get("commands", []):
            if not cmd.get("success", False):
                errors.append(f"Command failed: {cmd.get('name')} - {cmd.get('error')}")

        # 6. Check research requirement
        if validation_rules.get("research_required", False):
            research_results = execution_results.get("research", [])
            # Also consider research done in previous passes of the same stage
            state_research = state.get("research_results", [])
            all_research = research_results + state_research
            
            if not all_research:
                errors.append("Research was required but not requested or performed.")
            else:
                success_research = any(not self.validate_research_result(r) for r in all_research)
                
                if not success_research:
                    latest_errors = self.validate_research_result(all_research[-1])
                    errors.append("Mandatory research failed to meet quality metrics: " + "; ".join(latest_errors))

        validators = {
            validator
            for manifest in skill_manifests
            for validator in manifest.get("validators", [])
        }
        if "research_quality" in validators and (stage == "researcher" or actions.get("research_requests")):
            all_research = execution_results.get("research", []) + state.get("research_results", [])
            if all_research and not any(not self.validate_research_result(r) for r in all_research):
                errors.append("Skill validator research_quality failed.")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    def _resolve_existing_artifact(self, rel_path):
        full_path = os.path.join(self.base_path, rel_path)
        if os.path.exists(full_path):
            return full_path
        return os.path.join(self.base_path, ".agent/Loop_Flow", os.path.basename(rel_path))

    def _find_satisfying_artifact(self, expected_rel_path, required_sections, actions, execution_results):
        candidates = [expected_rel_path]
        expected_basename = os.path.basename(expected_rel_path)

        for write in execution_results.get("writes", []):
            if write.get("success") and write.get("path"):
                candidates.append(write["path"])

        for write in actions.get("writes", []):
            if write.get("path"):
                candidates.append(write["path"])

        for artifact in actions.get("artifacts", []):
            name = artifact.get("name")
            if name:
                candidates.append(name)
                candidates.append(os.path.join(".agent/Loop_Flow", name))

        seen = set()
        fallback = None
        exact_match = None
        for candidate in candidates:
            full_path = self._resolve_existing_artifact(candidate)
            normalized = os.path.normcase(os.path.abspath(full_path))
            if normalized in seen or not os.path.exists(full_path):
                continue
            seen.add(normalized)
            if os.path.basename(candidate) == expected_basename:
                exact_match = full_path
                if self._has_required_sections(full_path, required_sections):
                    return full_path
                continue
            if self._has_required_sections(full_path, required_sections):
                fallback = full_path

        return fallback or exact_match

    def _has_required_sections(self, full_path, required_sections):
        if not required_sections:
            return os.path.exists(full_path)
        if not full_path.endswith(".md"):
            return False
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            return all(
                re.search(f"^#+\\s+.*?{re.escape(section)}", content, re.MULTILINE | re.IGNORECASE)
                for section in required_sections
            )
        except Exception:
            return False

    def _validate_sections(self, full_path, required_sections, label_path, prefix):
        errors = []
        if not required_sections or not full_path.endswith(".md"):
            return errors
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            for section in required_sections:
                if not re.search(f"^#+\\s+.*?{re.escape(section)}", content, re.MULTILINE | re.IGNORECASE):
                    errors.append(f"{prefix} '{section}' missing in {label_path}")
        except Exception as e:
            errors.append(f"Failed to read {label_path} for section validation: {str(e)}")
        return errors
