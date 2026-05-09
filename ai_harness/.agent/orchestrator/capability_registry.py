import os
import subprocess
import json
import urllib.request
import urllib.error

class CapabilityRegistry:
    def __init__(self, config=None):
        self.config = config or {}
        self.capabilities = {
            "koboldcpp": {
                "available": False,
                "chat_completions": False,
                "completions": False,
                "vision_input": False,
                "max_context_estimate": 32768,
                "model_name": "unknown",
                "error": None
            },
            "filesystem": {
                "read": True,
                "write": True,
                "patch": True
            },
            "commands": {
                "typecheck": False,
                "test": False,
                "dev_server": False,
                "git_status": False,
                "git_diff": False,
                "git_commit": False
            },
            "research": {
                "web_search": False,
                "web_fetch": False,
                "citations_required": True,
                "backend": None,
                "error": "No research backend configured."
            },
            "browser": {
                "available": False,
                "playwright": False,
                "chrome_devtools": False,
                "chrome_remote_debugging": False,
                "performance_trace": False
            },
            "multimodal": {
                "image_input_available": False,
                "audio_input_available": False,
                "screenshot_analysis_available": False
            }
        }

    def detect_all(self):
        self._detect_kobold()
        self._detect_commands()
        self._detect_research()
        self._detect_browser()
        return self.capabilities

    def _detect_kobold(self):
        kb_config = self.config.get("koboldcpp", {})
        base_url = kb_config.get("base_url")
        if not base_url:
            self.capabilities["koboldcpp"]["error"] = "No base_url in config."
            return

        try:
            # Probe model info
            req = urllib.request.Request(f"{base_url}/api/v1/model")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    self.capabilities["koboldcpp"]["available"] = True
                    self.capabilities["koboldcpp"]["model_name"] = data.get("result", "unknown")
            
            # Probe chat completions support
            req = urllib.request.Request(f"{base_url}/api/v1/generate/check", method="POST")
            try:
                with urllib.request.urlopen(req, timeout=2) as response:
                    self.capabilities["koboldcpp"]["completions"] = (response.status == 200)
            except:
                pass
                
        except Exception as e:
            self.capabilities["koboldcpp"]["available"] = False
            self.capabilities["koboldcpp"]["error"] = str(e)

    def _detect_commands(self):
        # We check common tools
        self.capabilities["commands"]["git_status"] = self._can_run(["git", "status", "--short"])
        self.capabilities["commands"]["git_diff"] = self.capabilities["commands"]["git_status"]
        
        # Check node_modules for local tools
        if os.path.exists("node_modules/.bin/tsc"):
            self.capabilities["commands"]["typecheck"] = True
        elif self._can_run(["tsc", "--version"]):
            self.capabilities["commands"]["typecheck"] = True
            
        if os.path.exists("node_modules/.bin/vitest"):
            self.capabilities["commands"]["test"] = True
        elif self._can_run(["vitest", "--version"]):
            self.capabilities["commands"]["test"] = True

    def _detect_research(self):
        from playwright_research import PlaywrightResearch
        
        pw = PlaywrightResearch(self.config.get("web_research", {}))
        
        # Playwright is the primary research backend
        if pw.is_available():
            self.capabilities["research"]["web_search"] = True
            self.capabilities["research"]["web_fetch"] = True
            self.capabilities["research"]["backend"] = "playwright"
            self.capabilities["research"]["error"] = None
        else:
            self.capabilities["research"]["web_search"] = False
            self.capabilities["research"]["web_fetch"] = False
            self.capabilities["research"]["backend"] = None
            self.capabilities["research"]["error"] = "No functional browser research backend (Playwright) found."


    def _detect_browser(self):
        from playwright_research import PLAYWRIGHT_AVAILABLE
        
        self.capabilities["browser"]["playwright"] = PLAYWRIGHT_AVAILABLE
        self.capabilities["browser"]["available"] = PLAYWRIGHT_AVAILABLE
        self.capabilities["browser"]["chrome_devtools"] = False # CDP disabled
        self.capabilities["browser"]["chrome_remote_debugging"] = False
        self.capabilities["browser"]["performance_trace"] = False

    def _can_run(self, cmd):
        try:
            # We don't use shell=True for detection to avoid side effects
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, timeout=2)
            return True
        except:
            return False

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.capabilities, f, indent=2)
