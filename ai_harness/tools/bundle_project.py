import os
from pathlib import Path
from datetime import datetime

def bundle_project():
    # Configuration
    root_dir = Path(".")
    src_dir = root_dir / "src"
    
    # Generate timestamp for output filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_dir = root_dir / "docs" / "backups"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"FULL_PROJECT_{timestamp}.txt"
    
    # Files to include at the start (in order)
    start_files = [
        root_dir / "index.html"
    ]
    
    # Files to ignore (e.g., binaries, hidden files, or the output file itself)
    ignored_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', 
        '.ttf', '.eot', '.mp3', '.wav', '.ogg', '.py', '.svg', '.map',
        '.bat', '.yaml', '.lock'
    }
    ignored_names = {
        ".gitignore", "FULL_PROJECT.txt", "bundle_project.py", ".vscode", 
        ".git", ".agent", ".agents", ".logs", "node_modules", "dist", 
        "build", "SVG", "svg", ".env", "package-lock.json", "yarn.lock", 
        "__pycache__", "pnpm-lock.yaml", "tools", "tests"
    }

    print(f"Bundling project files into {output_file}...")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # 1. Add index.html
            for file_path in start_files:
                if file_path.exists():
                    write_file_to_bundle(file_path, outfile)
                else:
                    print(f"Warning: {file_path} not found.")

            # 2. Add directories recursively
            include_dirs = [src_dir, root_dir / "data"]
            
            for folder in include_dirs:
                if folder.exists():
                    print(f"Adding directory: {folder}")
                    # Use rglob to get all files in folder
                    for file_path in sorted(folder.rglob('*')):
                        if file_path.is_file():
                            # Check if we should ignore this file
                            if file_path.suffix.lower() in ignored_extensions:
                                continue
                            if any(part in ignored_names for part in file_path.parts):
                                continue
                            if file_path.name in ignored_names:
                                continue
                            
                            write_file_to_bundle(file_path, outfile)
                else:
                    print(f"Warning: directory not found at {folder}")
        
        print(f"Bundling complete. Output: {output_file}")
        log_decision("Developer", "Project Bundling", f"Bundled project into {output_file}. Removed PowerShell dependency.")
        
    except Exception as e:
        print(f"Fatal error during bundling: {e}")

def write_file_to_bundle(file_path, outfile):
    print(f"Processing: {file_path}")
    header = "=" * 40 + "\n"
    header += f"// FILE: {file_path}\n"
    header += "=" * 40 + "\n"
    
    outfile.write(header)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as infile:
            outfile.write(infile.read())
            outfile.write("\n\n")
    except Exception as e:
        outfile.write(f"Error reading file: {e}\n\n")

def log_decision(identity, action, rationale):
    """
    Attempts to log to .agent/logs/ but falls back to .logs/decision_logs.md
    if permissions are denied.
    """
    timestamp = datetime.now().isoformat()
    log_entry = f"Decision Log: [{timestamp}] [{identity}] [{action}] [{rationale}]\n"
    
    log_dir = Path(".logs/logs")
    log_file = log_dir / f"{datetime.now().strftime('%Y%m%d')}_log.txt"
    
    try:
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except PermissionError:
        fallback_file = Path(".logs/decision_logs.md")
        with open(fallback_file, "a", encoding="utf-8") as f:
            if fallback_file.stat().st_size == 0:
                f.write("# Decision logs (Fallback)\n\n")
            f.write(f"- {log_entry}")
    except Exception as e:
        print(f"Logging failed: {e}")

if __name__ == "__main__":
    bundle_project()
