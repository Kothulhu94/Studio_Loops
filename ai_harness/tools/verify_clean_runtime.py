import os
import glob
import sys
import json
import shutil

def verify_clean_runtime():
    base_path = os.getcwd()
    # 1. Stale Artifact Checks
    patterns = [
        ".agent/Loop_Flow/*.md",
        ".agent/Loop_Flow/*.json",
        ".agent/Loop_Flow/context_packs/*.md",
        ".agent/Loop_Flow/research/*.md",
        ".agent/logs/**/*.json",
        ".agent/logs/**/*.txt",
        ".agent/logs/**/*.md",
        "test_final.txt",
        "tasklist.txt",
        "scratch/*.py",
        "scratch/*.txt"
    ]
    
    dirty = []
    for pattern in patterns:
        matches = glob.glob(os.path.join(base_path, pattern), recursive=True)
        for match in matches:
            if not match.endswith(".gitkeep"):
                dirty.append(match)
            
    # 2. Forbidden Terms & Proof Validation
    forbidden_terms = [
        "run_command", "browser_subagent", "take_memory_snapshot",
        "evaluate_script", "list_console_messages", "take_screenshot",
        "grep_search", "Commit Hash", "example.com", "chrome-devtools-mcp",
        "fallback_backend", "HARNESS_VERIFICATION_MODE", "mock_verification",
        "Backend: mock_verification", "browser_audit"
    ]
    
    check_dirs = [
        ".agent/workflows", ".agent/skills", ".agent/orchestrator", 
        "tools", "src", "docs", "scratch"
    ]
    files_to_check = [os.path.join(base_path, "README.md")]
    for dir_name in check_dirs:
        full_dir = os.path.join(base_path, dir_name)
        if os.path.exists(full_dir):
            for root, dirs, files in os.walk(full_dir):
                for file in files:
                    files_to_check.append(os.path.join(root, file))

    for path in files_to_check:
        if not os.path.exists(path): continue
        if path.endswith((".md", ".py", ".json", ".txt")):
            if os.path.basename(path) == "verify_clean_runtime.py": continue
            
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Forbidden terms
                    for term in forbidden_terms:
                        if term in content:
                            dirty.append(f"Forbidden term '{term}' in {path}")
                    
                    # Proof Validation
                    if "docs/verification" in path.replace("\\", "/"):
                        if "browser_research_mdn_requestanimationframe.md" in path:
                            required = ["Status", "complete", "Backend: playwright", "developer.mozilla.org", "requestAnimationFrame", "Canvas API"]
                            forbidden = ["mock_verification", "Status: blocked", "Status: failed", "Status: partial", "No findings recorded"]
                            for r in required:
                                if r not in content:
                                    dirty.append(f"Proof {path} missing required term: {r}")
                            for f in forbidden:
                                if f in content:
                                    dirty.append(f"Proof {path} contains forbidden term: {f}")
                        else:
                            if "Status: blocked" in content and "blocked_expected" not in path:
                                dirty.append(f"Invalid proof artifact (Status: blocked): {path}")
                            if "No findings recorded" in content and "blocked_expected" not in path:
                                dirty.append(f"Invalid proof artifact (Empty findings): {path}")
            except: pass

    # 3. Allowlist Integrity
    allowlist_path = os.path.join(base_path, ".agent/orchestrator/command_allowlist.json")
    if os.path.exists(allowlist_path):
        with open(allowlist_path, 'r') as f:
            allowlist = json.load(f)
            for cmd in allowlist.get("allowed_commands", []):
                parts = cmd["command"]
                # Check if the primary executable exists or is in path
                exe = parts[0].replace("{drive}", "C:")
                found = os.path.exists(os.path.join(base_path, exe)) or shutil.which(exe)
                
                # Resilient check for absolute portable paths
                if not found and ":" in exe:
                    basename = os.path.basename(exe)
                    found = shutil.which(basename)
                
                if not found:
                    dirty.append(f"Allowlisted command executable missing: {exe}")
                
                # If it's a relative path to a script in the repo, check its full path
                if not found and "/" in exe and not ":" in exe:
                    if not os.path.exists(os.path.join(base_path, exe)):
                        dirty.append(f"Allowlisted script missing: {exe}")

    if dirty:
        print("FAIL: Dirty runtime or codebase detected!")
        for item in dirty:
            print(f"  {item}")
        sys.exit(1)
    
    print("PASS: Runtime is clean.")
    return True

if __name__ == "__main__":
    if verify_clean_runtime():
        sys.exit(0)
    else:
        sys.exit(1)
