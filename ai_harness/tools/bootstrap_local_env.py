import subprocess
import sys
import os
import shutil
import json

def run_command(cmd, shell=True):
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_env():
    print("--- Environment Check ---")
    
    # Python
    py_ok, py_ver, _ = run_command(["python", "--version"])
    print(f"Python: {'OK (' + py_ver.strip() + ')' if py_ok else 'FAILED'}")
    
    # Pip
    pip_ok, pip_ver, _ = run_command(["python", "-m", "pip", "--version"])
    print(f"Pip: {'OK (' + pip_ver.strip() + ')' if pip_ok else 'FAILED'}")
    
    # Playwright
    try:
        from playwright.sync_api import sync_playwright
        print("Playwright Python Package: OK")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                browser.close()
            print("Playwright Chromium: OK")
        except Exception as e:
            print(f"Playwright Chromium: FAILED ({str(e)})")
    except ImportError:
        print("Playwright Python Package: FAILED (not installed)")

    # Node/NPM/NPX
    node_ok, node_ver, _ = run_command(["node", "--version"])
    print(f"Node: {'OK (' + node_ver.strip() + ')' if node_ok else 'FAILED'}")
    
    npm_ok, npm_ver, _ = run_command(["npm", "--version"])
    print(f"NPM: {'OK (' + npm_ver.strip() + ')' if npm_ok else 'FAILED'}")
    
    npx_ok, npx_ver, _ = run_command(["npx", "--version"])
    print(f"NPX: {'OK (' + npx_ver.strip() + ')' if npx_ok else 'FAILED'}")

    # Package.json / node_modules
    has_pkg = os.path.exists("package.json")
    has_mods = os.path.exists("node_modules")
    print(f"package.json: {'Found' if has_pkg else 'Not Found'}")
    print(f"node_modules: {'Found' if has_mods else 'Not Found'}")

    # TSC / Vitest
    if npx_ok:
        tsc_ok, tsc_ver, _ = run_command(["npx", "tsc", "--version"])
        print(f"TSC: {'OK (' + tsc_ver.strip() + ')' if tsc_ok else 'FAILED'}")
        
        vitest_ok, vitest_ver, _ = run_command(["npx", "vitest", "--version"])
        print(f"Vitest: {'OK (' + vitest_ver.strip() + ')' if vitest_ok else 'FAILED'}")
    else:
        print("TSC: SKIP (no npx)")
        print("Vitest: SKIP (no npx)")

    # KoboldCPP
    print("KoboldCPP Reachability: ", end="", flush=True)
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:5001/api/v1/model", timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print(f"OK ({data.get('result', 'unknown')})")
            else:
                print(f"FAILED (Status {response.status})")
    except Exception as e:
        print(f"FAILED ({str(e)})")

def install_python_deps():
    print("--- Installing Python Dependencies ---")
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found.")
        return
    success, out, err = run_command(["python", "-m", "pip", "install", "-r", "requirements.txt"])
    if success:
        print("Python dependencies installed successfully.")
    else:
        print(f"Failed to install python dependencies:\n{err}")

def install_playwright():
    print("--- Installing Playwright Chromium ---")
    success, out, err = run_command(["python", "-m", "playwright", "install", "chromium"])
    if success:
        print("Playwright Chromium installed successfully.")
    else:
        print(f"Failed to install Playwright Chromium:\n{err}")

def install_node_deps():
    print("--- Installing Node Dependencies ---")
    if not os.path.exists("package.json"):
        print("package.json not found. Skipping.")
        return
    success, out, err = run_command(["npm", "install"])
    if success:
        print("Node dependencies installed successfully.")
    else:
        print(f"Failed to install node dependencies:\n{err}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--install-python-deps", action="store_true")
    parser.add_argument("--install-playwright", action="store_true")
    parser.add_argument("--install-node-deps", action="store_true")
    
    args = parser.parse_args()
    
    if args.check:
        check_env()
    if args.install_python_deps:
        install_python_deps()
    if args.install_playwright:
        install_playwright()
    if args.install_node_deps:
        install_node_deps()
    
    if not any(vars(args).values()):
        parser.print_help()
