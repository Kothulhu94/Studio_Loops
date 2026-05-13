import os
import sys
import argparse
import json
import re

def get_context_map(root_dir, search_terms, stage=None):
    """
    Scans the repository for relevant files and line ranges.
    Returns a 'Pruned Context Map'.
    """
    context_map = {}
    
    # 1. Load Index if available for Semantic Scoring
    index_path = os.path.join(root_dir, ".agent/Loop_Flow/source_index.json")
    symbol_map = {}
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                if isinstance(index_data, list):
                    for item in index_data:
                        path = item.get("path")
                        symbols = item.get("symbols", [])
                        if path and symbols:
                            symbol_map[path] = [s.lower() for s in symbols]
        except:
            pass

    # 2. Heuristic search configuration
    ignore_dirs = {
        '.git', 'node_modules', '.agent/logs', '.agent/state', 
        '.agent/Loop_Flow/context_packs', '.agent/Loop_Flow/research',
        '.agent/bin', '.agent/orchestrator', '.agent/skills', '.agent/workflows',
        '.agent/scratch', 'logs', 'scratch', '__pycache__', '.pytest_cache', 
        '.venv', 'venv', 'dist', 'build', '.next', '.vitest'
    }
    ignore_patterns = [
        r'\.agent/logs/.*',
        r'logs/.*',
        r'scratch/.*',
        r'.*__pycache__/.*',
        r'.*\.pyc$',
        r'\.agent/Loop_Flow/context_packs/.*',
        r'\.agent/Loop_Flow/research/latest_.*',
        r'\.agent/Loop_Flow/test_.*',
        r'\.agent/Loop_Flow/fail_.*',
        r'package-lock\.json',
        r'yarn\.lock',
        r'pnpm-lock\.yaml',
        r'LICENSE.*',
        r'NOTICE.*',
        r'\.DS_Store',
        r'Thumbs\.db'
    ]

    # Stage-aware directory prioritization
    prioritized_dirs = []
    if stage in ["developer", "debug_dev", "qa_tester"]:
        prioritized_dirs = ["src", "tests", "data"]
    elif stage == "researcher":
        prioritized_dirs = ["docs", "src"]

    for root, dirs, files in os.walk(root_dir):
        # Filter dirs in-place to prune walk
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        rel_root = os.path.relpath(root, root_dir).replace("\\", "/")
        if any(rel_root == ignore or rel_root.startswith(ignore + "/") for ignore in ignore_dirs):
            continue
            
        for file in files:
            if file.endswith(('.pyc', '.pyo', '.exe', '.dll', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.bin', '.pdf')):
                continue
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, root_dir).replace("\\", "/")
            
            # Skip ignored patterns
            if any(re.search(pat, rel_path) for pat in ignore_patterns):
                continue
            
            # 3. Multi-tiered Scoring
            file_score = 0
            lowered_rel_path = rel_path.lower()
            
            for term in search_terms:
                term_lowered = term.lower()
                
                # Symbol Match (Highest priority)
                if rel_path in symbol_map:
                    if any(term_lowered in sym for sym in symbol_map[rel_path]):
                        file_score += 25
                
                # Filename Match
                if term_lowered in lowered_rel_path.split("/")[-1]:
                    file_score += 15
                elif term_lowered in lowered_rel_path:
                    file_score += 5
            
            # Prioritized Dir Bonus
            if prioritized_dirs:
                if any(rel_path.startswith(p + "/") for p in prioritized_dirs):
                    file_score += 5

            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    # Limit scan for huge files
                    scan_limit = 3000
                    scan_lines = lines[:scan_limit]
                    
                    matches = []
                    content_score = 0
                    for i, line in enumerate(scan_lines):
                        line_lowered = line.lower()
                        term_matches = [term for term in search_terms if term.lower() in line_lowered]
                        if term_matches:
                            content_score += len(term_matches)
                            # Include context lines
                            start = max(0, i - 3)
                            end = min(len(lines), i + 10)
                            matches.append(f"L{start+1}-L{end}")
                    
                    total_score = file_score + (content_score * 2)
                    
                    if total_score >= 10:
                        # Limit to top clusters and cap matches
                        context_map[rel_path] = list(set(matches))[:8]
            except:
                pass
                    
    # Sort by relevance (not easily possible with current dict return but we've improved selection)
    return context_map

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gather pruned context for the project.")
    parser.add_argument("terms", nargs="+", help="Search terms for context gathering.")
    parser.add_argument("--stage", help="Current orchestrator stage for prioritized scanning.")
    args = parser.parse_args()
    
    root = os.getcwd()
    print(f"--- Context Pruning Map (Stage: {args.stage or 'None'}) for: {args.terms} ---")
    results = get_context_map(root, args.terms, stage=args.stage)
    if not results:
        print("No matches found.")
    
    # Simple output format for ContextPruner to parse
    for path, ranges in results.items():
        print(f"{path}: {', '.join(ranges) if ranges else 'Full File'}")

