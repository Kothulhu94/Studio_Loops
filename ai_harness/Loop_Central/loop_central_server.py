#!/usr/bin/env python3
"""Local operator command center for Studio Loop and KoboldCPP activity."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import socket
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import re
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


UI_DIR = Path(__file__).resolve().parent
HARNESS_DIR = UI_DIR.parent
REPO_DIR = HARNESS_DIR.parent
CENTRAL_DIR = HARNESS_DIR / "logs" / "loop_central"
KOBOLD_LOG = CENTRAL_DIR / "kobold.log"
COMMAND_LOG = CENTRAL_DIR / "loop_central.log"
GENERATIONS_LOG = CENTRAL_DIR / "generations.jsonl"
CENTRAL_STATE = CENTRAL_DIR / "loop_central_state.json"
AGENT_STATE = HARNESS_DIR / ".agent" / "state" / "studio_loop_state.json"
AGENT_RUN_LOGS = HARNESS_DIR / ".agent" / "logs" / "orchestrator_runs"
ORCHESTRATOR_SCRIPT = HARNESS_DIR / ".agent" / "orchestrator" / "studio_loop.py"
DEFAULT_PORT = int(os.environ.get("LOOP_CENTRAL_PORT", os.environ.get("KOBOLD_WATCH_PORT", "8765")))

ORCHESTRATOR_COMMANDS = {
    "run": {"label": "Run", "payload": "task"},
    "auto": {"label": "Auto", "payload": "task"},
    "continue": {"label": "Continue", "payload": "none"},
    "step": {"label": "Step", "payload": "none"},
    "retry": {"label": "Retry", "payload": "none"},
    "repair": {"label": "Repair", "payload": "none"},
    "status": {"label": "Status", "payload": "none"},
    "reset": {"label": "Reset", "payload": "none"},
    "validate": {"label": "Validate", "payload": "none"},
    "context": {"label": "Context", "payload": "none"},
    "research": {"label": "Research", "payload": "text"},
    "capabilities": {"label": "Capabilities", "payload": "none"},
    "sessions": {"label": "Sessions", "payload": "none"},
    "session-status": {"label": "Session Status", "payload": "text"},
    "resume-session": {"label": "Resume Session", "payload": "text"},
    "archive-session": {"label": "Archive Session", "payload": "text"},
}

ORCH_PROCESS: subprocess.Popen | None = None
ORCH_LOCK = threading.Lock()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_files() -> None:
    CENTRAL_DIR.mkdir(parents=True, exist_ok=True)
    if not KOBOLD_LOG.exists():
        KOBOLD_LOG.write_text("", encoding="utf-8")
    if not COMMAND_LOG.exists():
        COMMAND_LOG.write_text("", encoding="utf-8")
    if not GENERATIONS_LOG.exists():
        GENERATIONS_LOG.write_text("", encoding="utf-8")
    if not CENTRAL_STATE.exists():
        write_json(
            CENTRAL_STATE,
            {
                "status": "idle",
                "updated_at": now_iso(),
                "note": "Loop_Central state is initialized.",
            },
        )


def write_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> dict | list | None:
    try:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def tail_text(path: Path, max_lines: int = 240, max_bytes: int = 180_000) -> str:
    try:
        if not path.exists():
            return ""
        size = path.stat().st_size
        with path.open("rb") as handle:
            handle.seek(max(0, size - max_bytes))
            text = handle.read().decode("utf-8", errors="replace")
        lines = text.splitlines()
        return "\n".join(lines[-max_lines:])
    except OSError as exc:
        return f"Could not read {path.name}: {exc}"


def tail_jsonl(path: Path, limit: int = 40, max_bytes: int = 1_000_000) -> list[dict]:
    try:
        if not path.exists():
            return []
        size = path.stat().st_size
        with path.open("rb") as handle:
            handle.seek(max(0, size - max_bytes))
            text = handle.read().decode("utf-8", errors="replace")
    except OSError:
        return []

    rows = []
    for line in text.splitlines()[-limit * 3 :]:
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows[-limit:]


def compact_text(value, max_chars: int = 80_000) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, indent=2, ensure_ascii=False)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[truncated by Loop_Central]"


def newest_agent_pair() -> dict | None:
    if not AGENT_RUN_LOGS.exists():
        return None
    prompt_files = sorted(AGENT_RUN_LOGS.glob("*_prompt.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for prompt_path in prompt_files:
        prefix = prompt_path.name[: -len("_prompt.json")]
        response_path = AGENT_RUN_LOGS / f"{prefix}_response.txt"
        if not response_path.exists():
            continue
        prompt = read_json(prompt_path)
        try:
            response = response_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            response = ""
        return {
            "timestamp": datetime.fromtimestamp(max(prompt_path.stat().st_mtime, response_path.stat().st_mtime)).isoformat(timespec="seconds"),
            "source": "studio_loop_orchestrator",
            "prompt": prompt,
            "prompt_text": compact_text(prompt),
            "response": response,
            "prompt_path": str(prompt_path),
            "response_path": str(response_path),
        }
    return None


def history_from_agent_logs(limit: int = 20) -> list[dict]:
    if not AGENT_RUN_LOGS.exists():
        return []
    items = []
    prompt_files = sorted(AGENT_RUN_LOGS.glob("*_prompt.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for prompt_path in prompt_files[:limit]:
        prefix = prompt_path.name[: -len("_prompt.json")]
        response_path = AGENT_RUN_LOGS / f"{prefix}_response.txt"
        if not response_path.exists():
            continue
        prompt = read_json(prompt_path)
        try:
            response = response_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            response = ""
        items.append(
            {
                "timestamp": datetime.fromtimestamp(max(prompt_path.stat().st_mtime, response_path.stat().st_mtime)).isoformat(timespec="seconds"),
                "source": "studio_loop_orchestrator",
                "prompt_text": compact_text(prompt, 20_000),
                "response": compact_text(response, 30_000),
                "prompt_path": str(prompt_path),
                "response_path": str(response_path),
            }
        )
    return list(reversed(items))


def probe_kobold(port: int) -> dict:
    base = f"http://127.0.0.1:{port}"
    probes = [
        ("model", f"{base}/api/v1/model"),
        ("models", f"{base}/v1/models"),
        ("version", f"{base}/api/extra/version"),
    ]
    result = {"reachable": False, "base_url": base, "checked_at": now_iso()}
    for name, url in probes:
        try:
            with urllib.request.urlopen(url, timeout=0.45) as response:
                body = response.read(120_000).decode("utf-8", errors="replace")
                data = json.loads(body) if body else {}
                result.update({"reachable": True, "probe": name, "status_code": response.status, "data": data})
                if isinstance(data, dict):
                    result["model"] = data.get("result") or data.get("model") or data.get("object") or data.get("data")
                return result
        except (urllib.error.URLError, TimeoutError, socket.timeout, json.JSONDecodeError, OSError) as exc:
            result["error"] = str(exc)
    return result


def parse_kobold_events(max_lines: int = 500) -> list[dict]:
    """Parse KV cache and context shifting events from kobold.log."""
    if not KOBOLD_LOG.exists():
        return []
    
    events = []
    # Patterns to match
    # 1. [Context Shifting: Erased 1025 tokens at position 495]
    re_shift = re.compile(r"\[Context Shifting: Erased (\d+) tokens at position (\d+)\]")
    # 2. Processing Prompt [BATCH] (483 / 483 tokens)
    re_batch = re.compile(r"Processing Prompt \[BATCH\] \((\d+) / (\d+) tokens\)")
    # 3. apply_ubatch: purging positions [491, 494] of sequence 0 from KV cache
    re_purge = re.compile(r"apply_ubatch: purging positions \[(\d+), (\d+)\] of sequence (\d+) from KV cache")
    # 4. Generating (32 / 5000 tokens)
    re_gen = re.compile(r"Generating \((\d+) / (\d+) tokens\)")

    try:
        content = tail_text(KOBOLD_LOG, max_lines=max_lines)
        for line in content.splitlines():
            # Shift
            m = re_shift.search(line)
            if m:
                events.append({
                    "type": "context_shift",
                    "tokens": int(m.group(1)),
                    "pos": int(m.group(2)),
                    "text": line.strip()
                })
                continue
            
            # Batch
            m = re_batch.search(line)
            if m:
                events.append({
                    "type": "batch_processing",
                    "current": int(m.group(1)),
                    "total": int(m.group(2)),
                    "text": line.strip()
                })
                continue
            
            # Purge
            m = re_purge.search(line)
            if m:
                events.append({
                    "type": "kv_purge",
                    "start": int(m.group(1)),
                    "end": int(m.group(2)),
                    "seq": int(m.group(3)),
                    "text": line.strip()
                })
                continue

            # Gen
            m = re_gen.search(line)
            if m:
                # We only care about generation if it's part of a sequence of events
                events.append({
                    "type": "generation",
                    "current": int(m.group(1)),
                    "total": int(m.group(2)),
                    "text": line.strip()
                })
    except Exception:
        pass
    
    return events[-30:] # Keep last 30 events


def build_snapshot(port: int) -> dict:
    ensure_files()
    central_state = read_json(CENTRAL_STATE) or {}
    agent_state = read_json(AGENT_STATE) or {}
    history = tail_jsonl(GENERATIONS_LOG, limit=50)
    if not history:
        history = history_from_agent_logs(limit=25)
    current = history[-1] if history else newest_agent_pair()
    return {
        "generated_at": now_iso(),
        "paths": {
            "repo": str(REPO_DIR),
            "logs": str(CENTRAL_DIR),
            "kobold_log": str(KOBOLD_LOG),
            "central_log": str(COMMAND_LOG),
            "generations": str(GENERATIONS_LOG),
            "central_state": str(CENTRAL_STATE),
        },
        "kobold": probe_kobold(port),
        "orchestrator": {
            "commands": ORCHESTRATOR_COMMANDS,
            "running": orchestrator_running(),
            "process_dead": agent_state.get("active") and not orchestrator_running(),
        },
        "central_state": central_state,
        "agent_state": agent_state,
        "current": current or {},
        "history": history,
        "kv_events": parse_kobold_events(),
        "logs": {
            "kobold": tail_text(KOBOLD_LOG),
            "central": tail_text(COMMAND_LOG, max_lines=260),
        },
    }


def update_launch_state(args: argparse.Namespace) -> None:
    if not args.model_label and not args.model_path:
        return
    ensure_files()
    state = read_json(CENTRAL_STATE)
    if not isinstance(state, dict):
        state = {}
    state.update(
        {
            "status": "launcher_started",
            "model_label": args.model_label or state.get("model_label"),
            "model_path": args.model_path or state.get("model_path"),
            "kobold_port": args.kobold_port,
            "updated_at": now_iso(),
        }
    )
    write_json(CENTRAL_STATE, state)
    append_central_log(
        f"\n[{now_iso()}] Loop_Central opened for {state.get('model_label', 'KoboldCPP')} on port {args.kobold_port}.\n"
    )


def append_central_log(message: str) -> None:
    ensure_files()
    with COMMAND_LOG.open("a", encoding="utf-8") as handle:
        handle.write(message)
        if not message.endswith("\n"):
            handle.write("\n")


def append_kobold_log(message: str) -> None:
    ensure_files()
    with KOBOLD_LOG.open("a", encoding="utf-8") as handle:
        handle.write(message)
        if not message.endswith("\n"):
            handle.write("\n")


def orchestrator_running() -> bool:
    with ORCH_LOCK:
        return ORCH_PROCESS is not None and ORCH_PROCESS.poll() is None


def start_orchestrator_command(command: str, payload: str = "") -> tuple[int, dict]:
    if command not in ORCHESTRATOR_COMMANDS:
        return 400, {"ok": False, "error": "Unsupported orchestrator command."}
    if not ORCHESTRATOR_SCRIPT.exists():
        return 500, {"ok": False, "error": f"Missing orchestrator script: {ORCHESTRATOR_SCRIPT}"}

    payload = (payload or "").strip()
    payload_mode = ORCHESTRATOR_COMMANDS[command]["payload"]
    if payload_mode in ("task", "text") and not payload:
        return 400, {"ok": False, "error": f"{command} requires input text."}

    with ORCH_LOCK:
        global ORCH_PROCESS
        if ORCH_PROCESS is not None and ORCH_PROCESS.poll() is None:
            return 409, {"ok": False, "error": "A Studio Loop command is already running."}

        args = [sys.executable, str(ORCHESTRATOR_SCRIPT), command]
        if payload_mode != "none":
            args.append(payload)

        append_central_log(
            "\n"
            f"[{now_iso()}] $ python .agent/orchestrator/studio_loop.py {command}"
            f"{' ' + json.dumps(payload) if payload_mode != 'none' else ''}\n"
        )
        log_handle = COMMAND_LOG.open("a", encoding="utf-8")
        try:
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            ORCH_PROCESS = subprocess.Popen(
                args,
                cwd=str(HARNESS_DIR),
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=creationflags,
            )
        except OSError as exc:
            log_handle.close()
            append_central_log(f"[{now_iso()}] Failed to start Studio Loop command: {exc}\n")
            return 500, {"ok": False, "error": str(exc)}

        threading.Thread(target=finish_orchestrator_command, args=(ORCH_PROCESS, log_handle), daemon=True).start()
        return 202, {"ok": True, "command": command, "pid": ORCH_PROCESS.pid}


def finish_orchestrator_command(process: subprocess.Popen, log_handle) -> None:
    code = process.wait()
    log_handle.close()
    with ORCH_LOCK:
        global ORCH_PROCESS
        if ORCH_PROCESS is process:
            ORCH_PROCESS = None
    append_central_log(f"[{now_iso()}] Studio Loop command exited with code {code}.\n")


def stop_orchestrator_command() -> tuple[int, dict]:
    with ORCH_LOCK:
        process = ORCH_PROCESS
        if process is None or process.poll() is not None:
            return 200, {"ok": True, "message": "No Studio Loop command is running."}
        pid = process.pid
        process.terminate()

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)

    append_central_log(f"[{now_iso()}] Studio Loop command killed from Loop_Central (pid {pid}).\n")
    return 200, {"ok": True, "pid": pid}


def stop_kobold_processes() -> tuple[int, dict]:
    ensure_files()
    args = ["taskkill", "/IM", "koboldcpp.exe", "/F"]
    try:
        result = subprocess.run(args, cwd=str(REPO_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        append_kobold_log(f"[{now_iso()}] Stop model failed: {exc}\n")
        return 500, {"ok": False, "error": str(exc)}

    append_kobold_log(f"\n[{now_iso()}] Stop model requested from Loop_Central.\n")
    if result.stdout:
        append_kobold_log(result.stdout)
    if result.stderr:
        append_kobold_log(result.stderr)
    if result.returncode not in (0, 128):
        return 500, {"ok": False, "returncode": result.returncode, "output": result.stdout + result.stderr}
    return 200, {"ok": True, "returncode": result.returncode, "output": result.stdout + result.stderr}


class CentralHandler(BaseHTTPRequestHandler):
    server_version = "LoopCentral/1.0"

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        print(f"[{now_iso()}] GET {path}")
        
        # 1. Main entry points
        if path in ("", "/", "/index.html"):
            self.serve_file(UI_DIR / "index.html")
            return
            
        # 2. API endpoints (handle optional trailing slashes)
        clean_path = path.rstrip("/")
        if clean_path == "/api/snapshot":
            self.send_json(build_snapshot(self.server.kobold_port))
            return
        if clean_path == "/api/orchestrator/commands":
            self.send_json({"commands": ORCHESTRATOR_COMMANDS})
            return
        if clean_path == "/api/health":
            self.send_json({"ok": True, "time": now_iso()})
            return
        if clean_path == "/api/diagnostics":
            self.send_json(run_diagnostics(self.server.kobold_port))
            return
            
        # 3. Static assets
        rel_path = path.lstrip("/")
        if rel_path.startswith("ui/"):
            rel_path = rel_path[3:]
            
        requested = (UI_DIR / rel_path).resolve()
        
        try:
            # Security check: ensure the file is within UI_DIR
            # We use lower() for Windows case-insensitivity
            if str(requested).lower().startswith(str(UI_DIR).lower()):
                if requested.is_file():
                    self.serve_file(requested)
                    return
                elif (requested / "index.html").is_file():
                    self.serve_file(requested / "index.html")
                    return
            
            print(f"[{now_iso()}] 404 Not Found: {path} (resolved to {requested})")
            self.send_error(404, f"File not found: {path}")
        except Exception as exc:
            print(f"[{now_iso()}] 500 Server Error: {path} -> {exc}")
            self.send_error(500, str(exc))

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/orchestrator/command":
            data = self.read_body_json()
            if data is None:
                self.send_json({"ok": False, "error": "Invalid JSON body."}, status=400)
                return
            status, result = start_orchestrator_command(str(data.get("command", "")), str(data.get("payload", "")))
            self.send_json(result, status=status)
            return
        if parsed.path == "/api/orchestrator/stop":
            status, result = stop_orchestrator_command()
            self.send_json(result, status=status)
            return
        if parsed.path == "/api/model/stop":
            status, result = stop_kobold_processes()
            self.send_json(result, status=status)
            return
        if parsed.path == "/api/diagnostics":
            self.send_json(run_diagnostics(self.server.kobold_port))
            return
        self.send_json({"ok": False, "error": "Not found."}, status=404)

    def log_message(self, fmt: str, *args) -> None:
        return

    def read_body_json(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(min(length, 200_000))
            data = json.loads(body.decode("utf-8") or "{}")
            return data if isinstance(data, dict) else None
        except (ValueError, json.JSONDecodeError, OSError):
            return None

    def send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, path: Path) -> None:
        try:
            body = path.read_bytes()
        except OSError:
            self.send_error(404, "Not found")
            return
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_diagnostics(port: int) -> dict:
    results = []
    
    # 1. Kobold Check
    kobold = probe_kobold(port)
    results.append({
        "name": "KoboldCPP Connectivity",
        "status": "PASS" if kobold["reachable"] else "FAIL",
        "message": f"Connected to {kobold['base_url']}" if kobold["reachable"] else f"Could not reach KoboldCPP at {kobold['base_url']}. Make sure it is running."
    })
    
    # 2. GDD Check
    gdd_path = HARNESS_DIR / "docs" / "GDD_Surface_Terraforming.md"
    results.append({
        "name": "Game Design Document",
        "status": "PASS" if gdd_path.exists() else "WARN",
        "message": "GDD found and aligned." if gdd_path.exists() else "Missing GDD_Surface_Terraforming.md in docs/. This may cause model drift."
    })
    
    # 3. Log Health
    log_size = COMMAND_LOG.stat().st_size if COMMAND_LOG.exists() else 0
    results.append({
        "name": "Log Health",
        "status": "PASS" if log_size < 50_000_000 else "WARN",
        "message": f"Log size: {log_size / 1024 / 1024:.1f} MB." + (" Consider resetting logs." if log_size > 50_000_000 else "")
    })
    
    # 4. Orchestrator State
    agent_state = read_json(AGENT_STATE) or {}
    results.append({
        "name": "Orchestrator State",
        "status": "PASS" if agent_state.get("active") else "INFO",
        "message": f"Active session: {agent_state.get('feature_slug', 'None')}" if agent_state.get("active") else "No active feature loop running."
    })
    
    return {
        "timestamp": now_iso(),
        "checks": results,
        "summary": "System Healthy" if all(c["status"] in ("PASS", "INFO") for c in results) else "Issues Detected"
    }


class CentralServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, handler, kobold_port: int):
        super().__init__(server_address, handler)
        self.kobold_port = kobold_port


def port_is_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Open Loop_Central, the local Studio Loop command center.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--kobold-port", type=int, default=5001)
    parser.add_argument("--open", action="store_true", help="Open Loop_Central in the default browser.")
    parser.add_argument("--model-label", default="")
    parser.add_argument("--model-path", default="")
    args = parser.parse_args()

    ensure_files()
    update_launch_state(args)

    url = f"http://{args.host}:{args.port}/"
    if port_is_open(args.port):
        if args.open:
            webbrowser.open(url)
        print(f"Loop_Central is already running at {url}")
        return 0

    server = CentralServer((args.host, args.port), CentralHandler, args.kobold_port)
    if args.open:
        threading.Timer(0.35, lambda: webbrowser.open(url)).start()
    print(f"Loop_Central listening at {url}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
