#!/usr/bin/env python3
"""Replay parsing and validation for a logged Studio Loop model response."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


TARGET_FILE_RE = re.compile(r"^### Target File:\s+(.+?)\s*$", re.MULTILINE)


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


def latest_pair(root: Path) -> tuple[Path, Path]:
    runs_dir = root / ".agent" / "logs" / "orchestrator_runs"
    prompt_files = sorted(runs_dir.glob("*_prompt.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    for prompt_path in prompt_files:
        prefix = prompt_path.name[: -len("_prompt.json")]
        response_path = runs_dir / f"{prefix}_response.txt"
        if response_path.exists():
            return prompt_path, response_path
    raise FileNotFoundError(f"No prompt/response pair found in {runs_dir}")


def pair_from_prefix(root: Path, prefix: str) -> tuple[Path, Path]:
    runs_dir = root / ".agent" / "logs" / "orchestrator_runs"
    clean = prefix
    if clean.endswith("_prompt.json"):
        clean = clean[: -len("_prompt.json")]
    if clean.endswith("_response.txt"):
        clean = clean[: -len("_response.txt")]
    prompt_path = runs_dir / f"{clean}_prompt.json"
    response_path = runs_dir / f"{clean}_response.txt"
    if not prompt_path.exists() or not response_path.exists():
        raise FileNotFoundError(f"Missing prompt/response pair for prefix {prefix!r} in {runs_dir}")
    return prompt_path, response_path


def explicit_pair(prompt: str, response: str) -> tuple[Path, Path]:
    prompt_path = Path(prompt).resolve()
    response_path = Path(response).resolve()
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    if not response_path.exists():
        raise FileNotFoundError(f"Response file not found: {response_path}")
    return prompt_path, response_path


def extract_target_files(prompt_text: str) -> list[str]:
    seen = set()
    targets = []
    for match in TARGET_FILE_RE.finditer(prompt_text or ""):
        path = match.group(1).strip()
        if path not in seen:
            seen.add(path)
            targets.append(path)
    return targets


def load_parser(root: Path):
    orchestrator_dir = root / ".agent" / "orchestrator"
    sys.path.insert(0, str(orchestrator_dir))
    from response_parser import ResponseParser

    return ResponseParser(schema_path=str(orchestrator_dir / "actions_schema.json"))


def replay(root: Path, prompt_path: Path, response_path: Path) -> dict:
    root = Path(root)
    prompt_path = Path(prompt_path)
    response_path = Path(response_path)
    prompt_packet = load_json(prompt_path)
    if not isinstance(prompt_packet, dict):
        raise ValueError(f"Prompt file is not a JSON object: {prompt_path}")
    response_text = response_path.read_text(encoding="utf-8", errors="replace")
    prompt_text = str(prompt_packet.get("user", ""))

    parser = load_parser(root)
    parsed = parser.parse(response_text)
    actions = parsed.get("actions")
    is_valid, error = parser.validate_actions(actions)
    if actions is None:
        actions = {}

    telemetry = prompt_packet.get("telemetry") if isinstance(prompt_packet.get("telemetry"), dict) else {}
    return {
        "prompt_path": str(prompt_path),
        "response_path": str(response_path),
        "prompt_chars": len(prompt_text),
        "response_chars": len(response_text),
        "telemetry": {
            "stage": telemetry.get("stage"),
            "final_user_chars": telemetry.get("final_user_chars"),
            "max_prompt_chars": telemetry.get("max_prompt_chars"),
            "truncation_count": len(telemetry.get("truncations", [])) if isinstance(telemetry.get("truncations"), list) else 0,
        },
        "target_files": extract_target_files(prompt_text),
        "parsed": parsed.get("actions") is not None,
        "valid": is_valid,
        "validation_error": error,
        "stage": actions.get("stage"),
        "status": actions.get("status"),
        "summary": actions.get("summary"),
        "counts": {
            "writes": len(actions.get("writes", []) or []),
            "patches": len(actions.get("patches", []) or []),
            "commands": len(actions.get("commands", []) or []),
            "research_requests": len(actions.get("research_requests", []) or []),
            "risks": len(actions.get("risks", []) or []),
            "blockers": len(actions.get("blockers", []) or []),
        },
        "writes": [item.get("path") for item in actions.get("writes", []) if isinstance(item, dict)],
        "patches": [item.get("path") for item in actions.get("patches", []) if isinstance(item, dict)],
        "commands": [item.get("name") for item in actions.get("commands", []) if isinstance(item, dict)],
        "research_requests": [
            {
                "query": item.get("query"),
                "mode": item.get("mode"),
                "audit_kind": item.get("audit_kind"),
                "target_files": item.get("target_files", []),
            }
            for item in actions.get("research_requests", [])
            if isinstance(item, dict)
        ],
    }


def print_human(report: dict) -> None:
    print("Replay Report")
    print(f"Prompt: {report['prompt_path']}")
    print(f"Response: {report['response_path']}")
    print(f"Prompt chars: {report['prompt_chars']}")
    print(f"Response chars: {report['response_chars']}")
    print(f"Parsed ACTIONS_JSON: {report['parsed']}")
    print(f"Valid actions: {report['valid']}")
    if report.get("validation_error"):
        print(f"Validation error: {report['validation_error']}")
    print(f"Stage/status: {report.get('stage') or 'unknown'} / {report.get('status') or 'unknown'}")
    if report.get("summary"):
        print(f"Summary: {report['summary']}")

    telemetry = report.get("telemetry") or {}
    if telemetry:
        print(
            "Telemetry: "
            f"stage={telemetry.get('stage')}, "
            f"prompt={telemetry.get('final_user_chars')}/{telemetry.get('max_prompt_chars')}, "
            f"truncations={telemetry.get('truncation_count')}"
        )

    print("\nCounts:")
    for name, count in (report.get("counts") or {}).items():
        print(f"- {name}: {count}")

    print("\nTarget files in prompt:")
    targets = report.get("target_files") or []
    if targets:
        for target in targets:
            print(f"- {target}")
    else:
        print("- none found")

    if report.get("writes"):
        print("\nWrites:")
        for path in report["writes"]:
            print(f"- {path}")
    if report.get("patches"):
        print("\nPatches:")
        for path in report["patches"]:
            print(f"- {path}")
    if report.get("commands"):
        print("\nCommands:")
        for command in report["commands"]:
            print(f"- {command}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.getcwd(), help="Workspace root, or a path inside it.")
    parser.add_argument("--latest", action="store_true", help="Replay the newest prompt/response pair.")
    parser.add_argument("--prefix", help="Run-log prefix, such as 20260513_014702.")
    parser.add_argument("--prompt", help="Explicit *_prompt.json path.")
    parser.add_argument("--response", help="Explicit *_response.txt path.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when ACTIONS_JSON is invalid.")
    args = parser.parse_args(argv)

    root = find_workspace_root(args.root)
    if args.prompt or args.response:
        if not args.prompt or not args.response:
            parser.error("--prompt and --response must be supplied together")
        prompt_path, response_path = explicit_pair(args.prompt, args.response)
    elif args.prefix:
        prompt_path, response_path = pair_from_prefix(root, args.prefix)
    else:
        prompt_path, response_path = latest_pair(root)

    report = replay(root, prompt_path, response_path)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)
    if args.strict and not report["valid"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
