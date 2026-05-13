#!/usr/bin/env python3
"""Summarize Studio Loop prompt context telemetry without calling the model."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


TARGET_FILE_RE = re.compile(r"^### Target File:\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def find_workspace_root(start: str | os.PathLike[str]) -> Path:
    path = Path(start).resolve()
    for candidate in [path, *path.parents]:
        if (candidate / ".agent" / "orchestrator").is_dir():
            return candidate
    return path


def load_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def latest_file(directory: Path, pattern: str) -> Path | None:
    if not directory.exists():
        return None
    files = [path for path in directory.glob(pattern) if path.is_file()]
    if not files:
        return None
    return max(files, key=lambda path: path.stat().st_mtime)


def latest_prompt_pair(root: Path) -> tuple[Path | None, Path | None]:
    runs_dir = root / ".agent" / "logs" / "orchestrator_runs"
    if not runs_dir.exists():
        return None, None
    prompt_files = sorted(runs_dir.glob("*_prompt.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    for prompt_path in prompt_files:
        prefix = prompt_path.name[: -len("_prompt.json")]
        response_path = runs_dir / f"{prefix}_response.txt"
        if response_path.exists():
            return prompt_path, response_path
    return (prompt_files[0], None) if prompt_files else (None, None)


def split_h2_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(H2_RE.finditer(text or ""))
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1).strip()] = text[start:end].strip()
    return sections


def extract_target_files(prompt_text: str) -> list[str]:
    seen = set()
    targets = []
    for match in TARGET_FILE_RE.finditer(prompt_text or ""):
        path = match.group(1).strip()
        if path not in seen:
            seen.add(path)
            targets.append(path)
    return targets


def extract_context_map_status(prompt_text: str) -> dict:
    sections = split_h2_sections(prompt_text)
    section = sections.get("Context Map Validation", "")
    status_match = re.search(r"Status:\s*([A-Za-z_ -]+)", section)
    errors = re.findall(r"Error:\s*(.+)", section)
    warnings = re.findall(r"Warning:\s*(.+)", section)
    target_match = re.search(r"Target files:\s*(\d+)", section)
    return {
        "present": bool(section),
        "status": status_match.group(1).strip() if status_match else None,
        "target_files": int(target_match.group(1)) if target_match else None,
        "errors": errors,
        "warnings": warnings,
    }


def build_report(root: Path) -> dict:
    root = Path(root)
    telemetry_dir = root / ".agent" / "logs" / "context_telemetry"
    telemetry_path = latest_file(telemetry_dir, "*.json")
    prompt_path, response_path = latest_prompt_pair(root)

    prompt_packet = load_json(prompt_path) if prompt_path else None
    prompt_text = ""
    prompt_telemetry = None
    if isinstance(prompt_packet, dict):
        prompt_text = str(prompt_packet.get("user", ""))
        prompt_telemetry = prompt_packet.get("telemetry")

    telemetry = load_json(telemetry_path) if telemetry_path else None
    if not isinstance(telemetry, dict) and isinstance(prompt_telemetry, dict):
        telemetry = prompt_telemetry

    if not isinstance(telemetry, dict):
        telemetry = {}

    final_chars = telemetry.get("final_user_chars") or len(prompt_text)
    max_chars = telemetry.get("max_prompt_chars")
    ratio = None
    if isinstance(max_chars, int) and max_chars > 0:
        ratio = round(final_chars / max_chars, 3)

    return {
        "workspace": str(root),
        "telemetry_path": str(telemetry_path) if telemetry_path else None,
        "prompt_path": str(prompt_path) if prompt_path else None,
        "response_path": str(response_path) if response_path else None,
        "stage": telemetry.get("stage"),
        "final_user_chars": final_chars,
        "max_prompt_chars": max_chars,
        "budget_ratio": ratio,
        "raw_section_chars": telemetry.get("raw_section_chars", {}),
        "budgeted_section_chars": telemetry.get("budgeted_section_chars", {}),
        "truncations": telemetry.get("truncations", []),
        "target_files": extract_target_files(prompt_text),
        "context_map_validation": extract_context_map_status(prompt_text),
        "middle_truncation_marker_found": "CONTEXT TRUNCATED BY ORCHESTRATOR" in prompt_text,
        "prompt_has_telemetry": isinstance(prompt_telemetry, dict),
    }


def print_human(report: dict) -> None:
    print("Context Report")
    print(f"Workspace: {report['workspace']}")
    print(f"Telemetry: {report['telemetry_path'] or 'not found'}")
    print(f"Prompt: {report['prompt_path'] or 'not found'}")
    print(f"Stage: {report.get('stage') or 'unknown'}")
    if report.get("max_prompt_chars"):
        print(
            f"Prompt size: {report['final_user_chars']} / {report['max_prompt_chars']} chars "
            f"({report['budget_ratio']})"
        )
    else:
        print(f"Prompt size: {report['final_user_chars']} chars")

    print("\nBudgeted sections:")
    sections = report.get("budgeted_section_chars") or {}
    if sections:
        for name, chars in sections.items():
            raw = (report.get("raw_section_chars") or {}).get(name)
            suffix = f" from {raw}" if raw is not None else ""
            print(f"- {name}: {chars}{suffix}")
    else:
        print("- no telemetry section sizes found")

    print("\nTruncations:")
    truncations = report.get("truncations") or []
    if truncations:
        for item in truncations[:12]:
            print(f"- {item.get('section')}: {item.get('from')} -> {item.get('to')}")
        if len(truncations) > 12:
            print(f"- ... {len(truncations) - 12} more")
    else:
        print("- none recorded")

    context_status = report.get("context_map_validation") or {}
    print("\nContext map:")
    print(f"- present: {context_status.get('present')}")
    print(f"- status: {context_status.get('status') or 'unknown'}")
    print(f"- target files reported: {context_status.get('target_files')}")
    for warning in context_status.get("warnings", [])[:5]:
        print(f"- warning: {warning}")
    for error in context_status.get("errors", [])[:5]:
        print(f"- error: {error}")

    print("\nTarget files in prompt:")
    targets = report.get("target_files") or []
    if targets:
        for target in targets:
            print(f"- {target}")
    else:
        print("- none found")

    print(f"\nMiddle truncation marker found: {report['middle_truncation_marker_found']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.getcwd(), help="Workspace root, or a path inside it.")
    parser.add_argument("--latest", action="store_true", help="Report on the latest context telemetry/prompt pair.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    root = find_workspace_root(args.root)
    report = build_report(root)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
