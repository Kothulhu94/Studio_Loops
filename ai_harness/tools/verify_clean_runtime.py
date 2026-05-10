import glob
import json
import os
import shutil
import sys


PROOF_PATH = os.path.join("docs", "verification", "browser_research_mdn_requestanimationframe.md")
BUNDLE_PATH = "ai_harness_bundle.txt"

RUNTIME_PATTERNS = [
    ".agent/Loop_Flow/*.md",
    ".agent/Loop_Flow/*.json",
    ".agent/Loop_Flow/context_packs/*.md",
    ".agent/Loop_Flow/research/*.md",
    ".agent/logs/**/*",
    ".agent/logs/**/*.json",
    ".agent/logs/**/*.txt",
    ".agent/logs/**/*.md",
]

BUNDLE_RUNTIME_FILE_PREFIXES = [
    "FILE: .agent\\Loop_Flow\\",
    "FILE: .agent/Loop_Flow/",
    "FILE: .agent\\logs\\",
    "FILE: .agent/logs/",
    "FILE: .agent\\state\\sessions\\",
    "FILE: .agent/state/sessions/",
    "FILE: .agent\\state\\studio_loop.lock",
    "FILE: .agent/state/studio_loop.lock",
]

PROOF_FORBIDDEN = [
    "Status: failed",
    "Status: partial",
    "Status: blocked",
    "No findings recorded",
    "VRDisplay",
    "XRSession",
    "WebXR",
    "Deprecated",
    "Experimental",
    "Non-standard",
    "Limited availability",
    "mock_verification",
    "HARNESS_VERIFICATION_MODE",
]

MOJIBAKE_MARKERS = [
    "\ufffd",
    "\u00c3",
    "\u00c2",
    "\u00e2\u20ac",
    "\u00e2\u20ac\u2122",
    "\u00e2\u20ac\u0153",
    "\u00e2\u20ac\u009d",
    "\u00e2\u20ac\u201d",
    "\u00e2\u20ac\u201c",
    "\u00f0\u0178",
    "\u00d8",
    "\u00d9",
    "\u00d0",
    "\u00d1",
]

NON_ASCII_PUNCTUATION = [
    "\u2018",
    "\u2019",
    "\u201c",
    "\u201d",
    "\u2014",
    "\u2013",
    "\u2026",
    "\u00a0",
]

PROOF_REQUIRED = [
    "Status",
    "complete",
    "Backend: playwright",
    "developer.mozilla.org",
    "Canvas",
    "requestAnimationFrame",
]

CANONICAL_GOOD_SOURCES = [
    "Window/requestAnimationFrame",
    "Canvas_API/Tutorial/Basic_animations",
    "CanvasRenderingContext2D",
]

PRODUCTION_FORBIDDEN = [
    "mock_verification",
]

WORKFLOW_SKILL_FORBIDDEN = [
    "Gemistein Protocol",
    "thought_process",
    "action tags",
    "artifact tags",
    "browser_subagent",
    "run_command",
    "chrome-devtools-mcp",
    "take_screenshot",
    "take_memory_snapshot",
    "list_console_messages",
    "PortablePython",
    "logs.bat",
    "tsc_build",
]


def _read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def _is_gitkeep(path):
    return os.path.basename(path) == ".gitkeep"


def _verify_runtime_clean(base_path, dirty):
    for pattern in RUNTIME_PATTERNS:
        for match in glob.glob(os.path.join(base_path, pattern), recursive=True):
            if os.path.isdir(match):
                continue
            if _is_gitkeep(match):
                continue
            rel = os.path.relpath(match, base_path).replace("\\", "/")
            dirty.append(f"Generated runtime artifact remains: {match}")

    sessions_dir = os.path.join(base_path, ".agent/state/sessions")
    if os.path.isdir(sessions_dir):
        for match in glob.glob(os.path.join(sessions_dir, "*.json")):
            try:
                session = json.loads(_read_text(match))
            except Exception as exc:
                dirty.append(f"Unreadable session state remains: {match}: {exc}")
                continue
            if session.get("active") or session.get("status") in {"running", "failed", "blocked"}:
                dirty.append(f"Active or non-archived runtime session remains: {match}")

    lock_path = os.path.join(base_path, ".agent/state/studio_loop.lock")
    if os.path.exists(lock_path):
        dirty.append(f"Runtime lock remains: {lock_path}")


def _verify_proof(base_path, dirty):
    proof = os.path.join(base_path, PROOF_PATH)
    if not os.path.exists(proof):
        dirty.append(f"Missing proof artifact: {proof}")
        return

    content = _read_text(proof)
    normalized = content.lower()

    for required in PROOF_REQUIRED:
        if required not in content:
            dirty.append(f"Proof missing required term: {required}")

    if "## status" not in normalized or "complete" not in normalized.split("## status", 1)[1].split("##", 1)[0]:
        dirty.append("Proof status section is not complete.")

    if not any(source in content for source in CANONICAL_GOOD_SOURCES):
        dirty.append(f"Proof missing canonical good source indicator: {CANONICAL_GOOD_SOURCES}")

    for forbidden in PROOF_FORBIDDEN:
        if forbidden in content:
            dirty.append(f"Proof contains forbidden content: {forbidden}")

    for marker in MOJIBAKE_MARKERS:
        if marker in content:
            dirty.append(f"Proof contains mojibake marker: {marker.encode('unicode_escape').decode('ascii')}")

    for marker in NON_ASCII_PUNCTUATION:
        if marker in content:
            dirty.append(f"Proof contains non-ASCII punctuation: {marker.encode('unicode_escape').decode('ascii')}")


def _verify_bundle(base_path, dirty):
    bundle = os.path.join(base_path, BUNDLE_PATH)
    if not os.path.exists(bundle):
        return

    content = _read_text(bundle)
    for marker in MOJIBAKE_MARKERS:
        if marker in content:
            dirty.append(f"Bundle contains mojibake marker: {marker.encode('unicode_escape').decode('ascii')}")
    for marker in NON_ASCII_PUNCTUATION:
        if marker in content:
            dirty.append(f"Bundle contains non-ASCII punctuation: {marker.encode('unicode_escape').decode('ascii')}")
    file_headers = [line.strip() for line in content.splitlines() if line.startswith("FILE: ")]
    for header in file_headers:
        for marker in BUNDLE_RUNTIME_FILE_PREFIXES:
            if header.startswith(marker):
                dirty.append(f"Bundle contains generated runtime file: {header}")


def _iter_production_text_files(base_path):
    roots = [".agent/workflows", ".agent/skills", ".agent/orchestrator", "tools", "src", "docs", "README.md"]
    for root in roots:
        full = os.path.join(base_path, root)
        if os.path.isfile(full):
            yield full
            continue
        if not os.path.isdir(full):
            continue
        for dirpath, dirnames, filenames in os.walk(full):
            dirnames[:] = [dirname for dirname in dirnames if dirname != "__pycache__"]
            for filename in filenames:
                if filename.endswith((".md", ".py", ".json", ".txt")):
                    yield os.path.join(dirpath, filename)


def _verify_production_terms(base_path, dirty):
    verifier_path = os.path.abspath(__file__)
    for path in _iter_production_text_files(base_path):
        abs_path = os.path.abspath(path)
        if abs_path == verifier_path:
            continue
        if os.path.normpath(os.path.relpath(path, base_path)).startswith(os.path.join("tests", "fixtures")):
            continue
        content = _read_text(path)
        for term in PRODUCTION_FORBIDDEN:
            if term in content:
                dirty.append(f"Production file contains forbidden term '{term}': {path}")


def _verify_workflow_skill_terms(base_path, dirty):
    roots = [".agent/workflows", ".agent/skills"]
    for root in roots:
        full = os.path.join(base_path, root)
        if not os.path.isdir(full):
            continue
        for dirpath, dirnames, filenames in os.walk(full):
            dirnames[:] = [dirname for dirname in dirnames if dirname != "__pycache__"]
            for filename in filenames:
                if not filename.endswith((".md", ".json", ".txt")):
                    continue
                path = os.path.join(dirpath, filename)
                content = _read_text(path)
                for term in WORKFLOW_SKILL_FORBIDDEN:
                    if term in content:
                        dirty.append(f"Workflow/skill file contains forbidden legacy term '{term}': {path}")


def _allowlist_part_points_to_repo_file(part):
    if "{drive}" in part or ":" in part or part.startswith("\\"):
        return False
    normalized = part.replace("\\", "/")
    if normalized.startswith("node_modules/"):
        return False
    return normalized.endswith((".py", ".js", ".cjs", ".mjs", ".json", ".md"))


def _verify_allowlist_targets(base_path, dirty):
    allowlist_path = os.path.join(base_path, ".agent", "orchestrator", "command_allowlist.json")
    if not os.path.exists(allowlist_path):
        dirty.append(f"Missing command allowlist: {allowlist_path}")
        return

    with open(allowlist_path, "r", encoding="utf-8") as handle:
        allowlist = json.load(handle)

    drive = os.path.splitdrive(base_path)[0] or "C:"
    path_tools = {"python", "npx", "node", "npm", "git"}
    for command in allowlist.get("allowed_commands", []):
        command_parts = command.get("command", [])
        if not command_parts:
            dirty.append(f"Allowlisted command has no command parts: {command.get('name')}")
            continue
        exe = command_parts[0]
        if exe in path_tools:
            if not shutil.which(exe):
                dirty.append(f"Allowlisted PATH command missing: {exe}")
        else:
            resolved_exe = exe.replace("{drive}", drive)
            if not (os.path.exists(resolved_exe) or shutil.which(resolved_exe)):
                dirty.append(f"Allowlisted command executable missing: {resolved_exe}")
        for part in command_parts[1:]:
            if _allowlist_part_points_to_repo_file(part):
                full_path = os.path.join(base_path, part)
                if not os.path.exists(full_path):
                    dirty.append(f"Allowlisted repository target missing: {part}")


def verify_clean_runtime():
    base_path = os.getcwd()
    dirty = []

    _verify_runtime_clean(base_path, dirty)
    _verify_proof(base_path, dirty)
    _verify_bundle(base_path, dirty)
    _verify_production_terms(base_path, dirty)
    _verify_workflow_skill_terms(base_path, dirty)
    _verify_allowlist_targets(base_path, dirty)

    if dirty:
        print("FAIL: Dirty runtime or invalid proof detected.")
        for item in dirty:
            print(f"  {item}")
        sys.exit(1)

    print("PASS: Runtime is clean.")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify_clean_runtime() else 1)
