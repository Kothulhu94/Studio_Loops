import json
import os
import re

class CopyrightGuard:
    def __init__(self, forbidden_terms_path=".agent/orchestrator/forbidden_ip_terms.json"):
        self.forbidden_terms_path = forbidden_terms_path
        self.forbidden_data = self._load_terms()

    def _load_terms(self):
        if os.path.exists(self.forbidden_terms_path):
            try:
                with open(self.forbidden_terms_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"game_facing_forbidden": [], "research_allowed": True}

    def scan_text(self, text, is_research=False):
        if is_research and self.forbidden_data.get("research_allowed", False):
            return []
            
        found_terms = []
        forbidden_list = self.forbidden_data.get("game_facing_forbidden", [])
        # Also support the old list format if it's there
        if not forbidden_list and isinstance(self.forbidden_data, dict):
            for k, v in self.forbidden_data.items():
                if isinstance(v, list) and k != "research_allowed":
                    forbidden_list.extend(v)

        for term in forbidden_list:
            # Case-insensitive whole word match
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_terms.append({"term": term, "category": "game_facing_forbidden"})
        return found_terms

    def transform_prompt(self, prompt_text):
        # Specific transformation for clone-like prompts as requested in Section 19
        if re.search(r"Dungeon Keeper.*clone", prompt_text, re.IGNORECASE):
            return "original sci-fi underground/asteroid-base management game inspired by general genre mechanics: indirect worker control, room construction, resource systems, invasion defense, research progression, traps, and emergent base simulation"

        # Implementation of concept transformation logic
        replacements = {
            r"Dungeon Keeper": "underground overlord sim",
            r"clone": "inspired original project"
        }
        
        transformed = prompt_text
        for pattern, replacement in replacements.items():
            transformed = re.sub(pattern, replacement, transformed, flags=re.IGNORECASE)
            
        return transformed

    def validate_content(self, content, is_research=False):
        violations = self.scan_text(content, is_research=is_research)
        if violations:
            return False, f"Copyright-protected terms detected: {', '.join([v['term'] for v in violations])}"
        return True, None

    def create_default_terms(self):
        default_terms = {
            "research_allowed": True,
            "game_facing_forbidden": [
                "Dungeon Keeper", "Dungeon Heart", "Horned Reaper", "Bile Demon", 
                "Portal Gem", "Imps", "Keeper", "Warlock", "Mistress", "Bullfrog"
            ]
        }
        with open(self.forbidden_terms_path, 'w') as f:
            json.dump(default_terms, f, indent=2)
        self.forbidden_data = default_terms
