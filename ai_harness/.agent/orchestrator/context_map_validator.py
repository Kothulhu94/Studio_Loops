import json
import os
import re
from dataclasses import dataclass, field


SOURCE_PATH_RE = re.compile(
    r"(?P<path>(?:src|public|tests|tools|data|docs|\.agent/orchestrator|\.agent/workflows|\.agent/skills)/"
    r"[A-Za-z0-9_./-]+\.(?:ts|tsx|js|jsx|css|html|json|py|md))"
)


@dataclass
class ContextMapValidation:
    valid: bool
    target_files: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    normalized_map: dict = field(default_factory=dict)
    changed: bool = False


class ContextMapValidator:
    GAME_ALLOWED_ROOTS = ("src", "tests", "data", "docs", "public")
    HARNESS_ALLOWED_ROOTS = (".agent/orchestrator", ".agent/workflows", ".agent/skills", "tests", "tools", "docs")

    def __init__(self, workspace_root):
        self.workspace_root = workspace_root

    def validate_file(self, context_map_path, stack_profile="game_source", candidate_text="", repair=True):
        if not context_map_path:
            return ContextMapValidation(False, errors=["No context_map.json path provided."])

        full_path = self._full_path(context_map_path)
        if not os.path.exists(full_path):
            return ContextMapValidation(False, errors=[f"Context map not found: {context_map_path}"])

        try:
            with open(full_path, "r", encoding="utf-8") as handle:
                raw_map = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            return ContextMapValidation(False, errors=[f"Context map is not valid JSON: {exc}"])

        result = self.validate_map(raw_map, stack_profile=stack_profile, candidate_text=candidate_text)
        if repair and result.target_files:
            normalized_text = json.dumps(result.normalized_map, indent=2)
            original_text = json.dumps(raw_map, indent=2)
            if normalized_text != original_text:
                try:
                    with open(full_path, "w", encoding="utf-8") as handle:
                        handle.write(normalized_text + "\n")
                    result.changed = True
                except OSError as exc:
                    result.warnings.append(f"Could not write normalized context map: {exc}")
        return result

    def validate_map(self, raw_map, stack_profile="game_source", candidate_text=""):
        errors = []
        warnings = []
        target_files = self._extract_targets(raw_map)
        if not target_files:
            promoted = self._promote_paths_from_text(candidate_text, stack_profile)
            if promoted:
                target_files = promoted
                warnings.append("No target_files found; promoted exact source paths from artifact text.")
            else:
                errors.append("Context map has no target_files, files, or pruned_context entries.")

        normalized_targets = []
        seen = set()
        for item in target_files:
            path = item.get("path") if isinstance(item, dict) else str(item)
            if isinstance(item, dict):
                reason = item.get("reason") or item.get("description") or "Referenced by context map."
                ranges = item.get("ranges")
            else:
                reason = "Referenced by context map."
                ranges = None
            normalized_path, path_error = self._normalize_path(path)
            if path_error:
                errors.append(path_error)
                continue
            if normalized_path in seen:
                continue
            seen.add(normalized_path)
            if not self._is_allowed_root(normalized_path, stack_profile):
                errors.append(f"Target file is outside allowed context roots for {stack_profile}: {normalized_path}")
                continue
            full_path = os.path.join(self.workspace_root, normalized_path)
            if not os.path.isfile(full_path):
                errors.append(f"Target file does not exist: {normalized_path}")
                continue
            entry = {"path": normalized_path, "reason": str(reason)}
            if ranges:
                entry["ranges"] = ranges
            normalized_targets.append(entry)

        normalized_map = dict(raw_map) if isinstance(raw_map, dict) else {}
        normalized_map["target_files"] = normalized_targets
        normalized_map.pop("files", None)
        normalized_map.pop("pruned_context", None)

        if not normalized_targets and not errors:
            errors.append("Context map validation produced no usable target files.")

        return ContextMapValidation(
            valid=not errors,
            target_files=normalized_targets,
            errors=errors,
            warnings=warnings,
            normalized_map=normalized_map,
        )

    def _extract_targets(self, raw_map):
        if not isinstance(raw_map, dict):
            return []
        for key in ("target_files", "files", "pruned_context"):
            value = raw_map.get(key)
            if isinstance(value, list) and value:
                return value
        return []

    def _promote_paths_from_text(self, text, stack_profile):
        promoted = []
        seen = set()
        for match in SOURCE_PATH_RE.finditer(text or ""):
            path = match.group("path").replace("\\", "/")
            if path in seen or not self._is_allowed_root(path, stack_profile):
                continue
            seen.add(path)
            promoted.append({"path": path, "reason": "Promoted from artifact text."})
            if len(promoted) >= 12:
                break
        return promoted

    def _normalize_path(self, path):
        rel_path = str(path or "").replace("\\", "/").strip()
        if not rel_path:
            return None, "Target file path is empty."
        normalized = os.path.normpath(rel_path).replace("\\", "/")
        if os.path.isabs(rel_path) or normalized == ".." or normalized.startswith("../") or "/../" in normalized:
            return None, f"Target file must be workspace-relative and cannot contain '..': {rel_path}"
        return normalized, None

    def _is_allowed_root(self, path, stack_profile):
        roots = self.HARNESS_ALLOWED_ROOTS if stack_profile == "harness_internal" else self.GAME_ALLOWED_ROOTS
        return any(path == root or path.startswith(root + "/") for root in roots)

    def _full_path(self, path):
        return path if os.path.isabs(path) else os.path.join(self.workspace_root, path)
