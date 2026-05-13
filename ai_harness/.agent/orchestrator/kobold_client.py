import requests
import json
import os
from datetime import datetime

class KoboldClientError(Exception):
    """Base error for local model client failures."""


class KoboldTransportError(KoboldClientError):
    """KoboldCPP could not be reached or did not respond in time."""


class KoboldResponseError(KoboldClientError):
    """KoboldCPP responded, but not with the expected chat-completion shape."""


class KoboldClient:
    def __init__(self, config, base_path=None):
        self.config = config["koboldcpp"]
        self.base_path = base_path or os.getcwd()
        self.logs_path = os.path.join(self.base_path, config["paths"]["logs"])
        self.connect_timeout = self.config.get("connect_timeout_seconds", 15)
        self.read_timeout = self.config.get("read_timeout_seconds", 900)

    def call(self, prompt_packet):
        url = f"{self.config['base_url']}{self.config['endpoint']}"
        payload = {
            "model": self.config["model"],
            "messages": [
                {"role": "system", "content": prompt_packet["system"]},
                {"role": "user", "content": prompt_packet["user"]}
            ],
            "temperature": self.config["temperature"],
            "top_p": self.config["top_p"],
            "max_tokens": self.config["max_output_tokens"]
        }

        try:
            response = requests.post(url, json=payload, timeout=(self.connect_timeout, self.read_timeout))
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Log the interaction
            self.log_interaction(prompt_packet, content)
            
            return content
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            message = (
                f"KoboldCPP transport failure at {url}: {e}. "
                f"Configured timeout=(connect={self.connect_timeout}s, read={self.read_timeout}s)."
            )
            print(message)
            raise KoboldTransportError(message) from e
        except requests.exceptions.RequestException as e:
            message = f"KoboldCPP HTTP/client failure at {url}: {e}"
            print(message)
            raise KoboldTransportError(message) from e
        except (KeyError, IndexError, TypeError, ValueError) as e:
            message = f"KoboldCPP response was not a valid chat completion: {e}"
            print(message)
            raise KoboldResponseError(message) from e
        except Exception as e:
            message = f"Unexpected KoboldCPP client failure: {e}"
            print(message)
            raise KoboldClientError(message) from e

    def log_interaction(self, prompt, response):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join(self.logs_path, "orchestrator_runs")
        os.makedirs(log_dir, exist_ok=True)
        
        with open(os.path.join(log_dir, f"{timestamp}_prompt.json"), 'w') as f:
            json.dump(prompt, f, indent=2)
        with open(os.path.join(log_dir, f"{timestamp}_response.txt"), 'w', encoding='utf-8') as f:
            f.write(response)

        self.log_watch_interaction(prompt, response, timestamp)

    def log_watch_interaction(self, prompt, response, timestamp):
        watch_dir = os.path.join(self.base_path, "logs", "loop_central")
        os.makedirs(watch_dir, exist_ok=True)

        prompt_text = json.dumps(prompt, indent=2, ensure_ascii=False)
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "source": "studio_loop",
            "prompt": prompt,
            "prompt_text": self._truncate_for_watch(prompt_text),
            "response": self._truncate_for_watch(response),
            "prompt_chars": len(prompt_text),
            "response_chars": len(response),
        }

        generations_path = os.path.join(watch_dir, "generations.jsonl")
        with open(generations_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        state_path = os.path.join(watch_dir, "loop_central_state.json")
        state = {
            "status": "model_response_captured",
            "updated_at": entry["timestamp"],
            "last_generation_timestamp": entry["timestamp"],
            "last_prompt_chars": entry["prompt_chars"],
            "last_response_chars": entry["response_chars"],
            "last_orchestrator_log_prefix": timestamp,
        }
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def _truncate_for_watch(self, text, max_chars=120000):
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[truncated for Kobold watch UI]"
