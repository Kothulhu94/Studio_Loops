# ROG Ally X Local Setup

This guide covers setting up the Studio Loop AI Harness on the internal SSD.

## Prerequisites

Ensure you have the following installed and in your PATH:

- Python 3.10+
- Node.js (Latest LTS recommended)
- Git

## Setup Flow

1. **Clone or move the repository** to `C:\Users\rchos\Desktop\Studio_Loop\ai_harness`.

2. **Install Python dependencies**:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m playwright install chromium
   ```

3. **Install Node dependencies** (if `package.json` is present):
   ```powershell
   npm install
   ```

4. **Verify the environment**:
   ```powershell
   python tools/bootstrap_local_env.py --check
   ```

5. **Verify research capabilities**:
   ```powershell
   python .agent/orchestrator/browser_research.py --check
   ```

6. **Check full capabilities**:
   ```powershell
   python .agent/orchestrator/studio_loop.py capabilities
   ```

7. **Run clean runtime verification**:
   ```powershell
   python tools/verify_clean_runtime.py
   ```

## Usage

- Keep the KoboldCPP terminal open and running your model.
- The KoboldCPP IPv6 warning is harmless if `127.0.0.1:5001` works.
- Use `run` first to test a single stage:
  ```powershell
  python .agent/orchestrator/studio_loop.py run "Create a tiny test blueprint..."
  ```
- Use `step` to execute one stage at a time.
- Use `auto` for fully autonomous operation once you've verified stability.

## Troubleshooting

- If Playwright fails to launch, run `python -m playwright install chromium` again.
- If commands are not found, ensure Python and Node are in your System PATH.
