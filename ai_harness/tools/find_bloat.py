import os
import sys
from pathlib import Path

def find_bloat():
    src_dir = Path("src")
    import json
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    threshold = 500
    violations = []
    
    if not src_dir.exists():
        if args.json: print(json.dumps([]))
        else: print("src directory not found. Skipping bloat check.")
        sys.exit(0)
        
    for file_path in src_dir.rglob("*"):
        if file_path.suffix in [".ts", ".tsx", ".js", ".jsx", ".css"]:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    count = len(lines)
                    if count > threshold:
                        violations.append({"path": str(file_path).replace("\\", "/"), "lines": count})
            except Exception as e:
                pass
    
    if args.json:
        print(json.dumps(violations))
    else:
        if violations:
            print("\nBLOAT DETECTED:")
            for v in violations:
                print(f"{v['path']}: {v['lines']} lines")
        else:
            print("No bloat detected.")
            
    sys.exit(1 if violations else 0)

if __name__ == "__main__":
    find_bloat()
