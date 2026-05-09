import json
import os
import re

class ArtifactValidator:
    def __init__(self, base_path):
        self.base_path = base_path

    def validate(self, stage, actions, execution_results, validation_rules, state):
        errors = []
        warnings = []

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
            full_path = os.path.join(self.base_path, req_file_processed)
            
            if not os.path.exists(full_path):
                # Fallback check in Loop_Flow
                full_path = os.path.join(self.base_path, ".agent/Loop_Flow", os.path.basename(req_file_processed))
            
            if not os.path.exists(full_path):
                errors.append(f"Required file missing: {req_file_processed}")
                continue

            # Check required sections if it's a markdown file
            if full_path.endswith(".md"):
                required_sections = validation_rules.get("required_sections", [])
                if required_sections:
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        for section in required_sections:
                            if not re.search(f"^#+\\s+.*?{re.escape(section)}", content, re.MULTILINE | re.IGNORECASE):
                                errors.append(f"Required section '{section}' missing in {req_file_processed}")
                    except Exception as e:
                        errors.append(f"Failed to read {req_file_processed} for section validation: {str(e)}")

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
                success_research = any(
                    r.get("status") == "complete"
                    and len(r.get("sources", [])) >= 2
                    and len(r.get("findings", [])) >= 2
                    and r.get("artifact_path")
                    for r in all_research
                )
                
                if not success_research:
                    errors.append("Mandatory research failed to meet quality metrics (Status: complete, Sources >= 2, Findings >= 2).")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
