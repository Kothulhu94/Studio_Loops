import os
import sys
import argparse
import json
import re

def get_context_map(root_dir, search_terms):
    """
    Scans the repository for relevant files and line ranges.
    Returns a 'Pruned Context Map'.
    """
    context_map = {}
    # 1. Try to use index if available
    index_path = os.path.join(root_dir, ".agent/state/source_index.json")
    indexed_files = []
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                indexed_files = index_data.get("files", [])
        except:
            pass

    # 2. Heuristic search
    ignore_dirs = {
        '.git', 'node_modules', '.agent/logs', '.agent/state', 
        '.agent/Loop_Flow/context_packs', '.agent/Loop_Flow/research'
    }
    ignore_patterns = [
        r'\.agent/logs/.*',
        r'\.agent/Loop_Flow/context_packs/.*',
        r'\.agent/Loop_Flow/research/latest_.*',
        r'\.agent/Loop_Flow/test_.*',
        r'\.agent/Loop_Flow/fail_.*',
        r'\.agent/Loop_Flow/multi_feature_.*',
        r'\.agent/Loop_Flow/feature_x_.*',
        r'\.agent/Loop_Flow/implement_feature_x_.*',
        r'test_final\.txt',
        r'tasklist\.txt'
    ]

    for root, dirs, files in os.walk(root_dir):
        # Filter dirs in-place to prune walk
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        rel_root = os.path.relpath(root, root_dir).replace("\\", "/")
        if any(rel_root == ignore or rel_root.startswith(ignore + "/") for ignore in ignore_dirs):
            continue
            
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, root_dir).replace("\\", "/")
            
            # Skip ignored patterns
            if any(re.search(pat, rel_path) for pat in ignore_patterns):
                continue
            if file == "test_final.txt" or file == "tasklist.txt":
                continue
                
            # Check filename relevance first
            file_score = 0
            for term in search_terms:
                if term.lower() in rel_path.lower():
                    file_score += 10
            
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    # Limit scan for huge files
                    if len(lines) > 2000:
                        lines = lines[:2000]
                    matches = []
                    for i, line in enumerate(lines):
                        line_matches = [term for term in search_terms if term.lower() in line.lower()]
                        if line_matches:
                            # Include context lines
                            start = max(0, i - 5)
                            end = min(len(lines), i + 15)
                            matches.append(f"L{start+1}-L{end}")
                    
                    if matches or file_score > 0:
                        context_map[rel_path] = list(set(matches))[:5] # Limit to top 5 clusters
            except:
                pass
                    
    return context_map

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gather pruned context for the project.")
    parser.add_argument("terms", nargs="+", help="Search terms for context gathering.")
    args = parser.parse_args()
    
    root = os.getcwd()
    print(f"--- Context Pruning Map for: {args.terms} ---")
    results = get_context_map(root, args.terms)
    if not results:
        print("No matches found.")
    for path, ranges in results.items():
        print(f"{path}: {', '.join(ranges) if ranges else 'Full File'}")
