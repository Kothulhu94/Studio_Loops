import requests
import json
import os
from datetime import datetime

class KoboldClient:
    def __init__(self, config):
        self.config = config["koboldcpp"]
        self.logs_path = config["paths"]["logs"]

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
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Log the interaction
            self.log_interaction(prompt_packet, content)
            
            return content
        except Exception as e:
            print(f"Error calling KoboldCPP: {e}")
            return f"Error: {str(e)}"

    def log_interaction(self, prompt, response):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join(self.logs_path, "orchestrator_runs")
        os.makedirs(log_dir, exist_ok=True)
        
        with open(os.path.join(log_dir, f"{timestamp}_prompt.json"), 'w') as f:
            json.dump(prompt, f, indent=2)
        with open(os.path.join(log_dir, f"{timestamp}_response.txt"), 'w', encoding='utf-8') as f:
            f.write(response)
