import glob
import json
import os
import shutil
import sys


PROOF_PATH = os.path.join("docs", "verification", "browser_research_mdn_requestanimationframe.md")

RUNTIME_PATTERNS = [
    ".agent/Loop_Flow/*.md",
    ".agent/Loop_Flow/*.json",
    ".agent/Loop_Flow/context_packs/*.md",
    ".agent/Loop_Flow/research/*.md",
    ".agent/logs/**/*.json",
    ".agent/logs/**/*.txt",
    ".agent/logs/**/*.md",
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
    "�",
    "Ã",
    "Â",
    "â€",
    "â€™",
    "â€œ",
    "â€",
    "â€”",
    "â€“",
    "ðŸ",
    "Ø",
    "Ù",
    "Ð",
    "Ñ",
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


def _read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def _is_gitkeep(path):
    return os.path.basename(path) == ".gitkeep"


def _verify_runtime_clean(base_path, dirty):
    live_research = glob.glob(os.path.join(base_path, ".agent/Loop_Flow/research/*_research_brief.md"))
    for pattern in RUNTIME_PATTERNS:
        for match in glob.glob(os.path.join(base_path, pattern), recursive=True):
            if not _is_gitkeep(match):
                rel = os.path.relpath(match, base_path).replace("\\", "/")
                if live_research and (
                    rel.startswith(".agent/Loop_Flow/research/")
                    or rel.startswith(".agent/logs/research/cache/")
                ):
                    continue
                dirty.append(f"Generated runtime artifact remains: {match}")


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
            dirty.append(f"Proof contains mojibake marker: {marker}")


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
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
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
    for cmd in allowlist.get("allowed_commands", []):
        command_parts = cmd.get("command", [])
        if not command_parts:
            dirty.append(f"Allowlisted command has no command parts: {cmd.get('name')}")
            continue
        exe = command_parts[0].replace("{drive}", drive)
        if not (os.path.exists(exe) or shutil.which(exe) or shutil.which(os.path.basename(exe))):
            dirty.append(f"Allowlisted command executable missing: {exe}")
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
    _verify_production_terms(base_path, dirty)
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
