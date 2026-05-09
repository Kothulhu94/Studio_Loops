import os
import glob
import sys

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
        "fallback_backend"
    ]
    
    check_dirs = [
        ".agent/workflows", ".agent/skills", ".agent/orchestrator", 
        "tools", "tests", "src", "docs", "scratch"
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
                        if "Status: blocked" in content and "blocked_expected" not in path:
                            dirty.append(f"Invalid proof artifact 