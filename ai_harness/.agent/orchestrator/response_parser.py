import json
import re
try:
    from jsonschema import validate as jsonschema_validate, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

class SchemaValidator:
    def __init__(self, schema_path):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)

    def validate(self, data):
        if not isinstance(data, dict):
            return False, "Data must be a JSON object."
        
        if JSONSCHEMA_AVAILABLE:
            try:
                jsonschema_validate(instance=data, schema=self.schema)
                return True, None
            except ValidationError as e:
                # Format error to be more readable for the model
                path = " -> ".join([str(p) for p in e.path]) if e.path else "root"
                return False, f"Schema validation failed at [{path}]: {e.message}"
        
        # Fallback manual validation (Basic)
        # 1. Required keys
        for key in self.schema.get("required", []):
            if key not in data:
                return False, f"Missing required key: {key}"
        
        # 2. Key Types & Enums
        properties = self.schema.get("properties", {})
        for key, value in data.items():
            if key not in properties:
                if self.schema.get("additionalProperties") is False:
                    return False, f"Unknown root field: {key}"
                continue
                
            spec = properties[key]
            
            # Check type
            spec_types = spec.get("type")
            if not isinstance(spec_types, list):
                spec_types = [spec_types]
                
            type_map = {
                "string": str,
                "object": dict,
                "array": list,
                "boolean": bool,
                "integer": int,
                "number": (int, float),
                "null": type(None)
            }
            
            match = False
            for t in spec_types:
                if t in type_map and isinstance(value, type_map[t]):
                    match = True
                    break
            
            if not match and "null" not in spec_types:
                return False, f"Key '{key}' must be one of {spec_types}."
            
            # Check enums
            if "enum" in spec and value not in spec["enum"]:
                return False, f"Invalid value for '{key}': {value}. Must be one of {spec['enum']}"
            
            # Sub-validation for arrays
            if "array" in spec_types and "items" in spec:
                item_spec = spec["items"]
                for i, item in enumerate(value):
                    if item_spec.get("type") == "object" and not isinstance(item, dict):
                        return False, f"Item {i} in '{key}' must be an object."
                    
                    if isinstance(item, dict):
                        for req_item_key in item_spec.get("required", []):
                            if req_item_key not in item:
                                return False, f"Item {i} in '{key}' missing required key: {req_item_key}"
                        
                        if item_spec.get("additionalProperties") is False:
                            item_props = item_spec.get("properties", {})
                            for k in item.keys():
                                if k not in item_props:
                                    return False, f"Unknown field '{k}' in {key}[{i}]"

        return True, None


class ResponseParser:
    def __init__(self, schema_path=None):
        self.validator = SchemaValidator(schema_path) if schema_path else None
        self.required_action_keys = {"stage", "status", "summary"}

    def _relaxed_json_loads(self, json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Try to fix common issues iteratively
            cleaned = json_str
            
            # 1. Fix invalid escapes: \ followed by a non-standard character
            cleaned = re.sub(r"\\(?![\\\"\/bfnrtu])", "", cleaned)
            
            # 2. Fix trailing commas: [1, 2, ] -> [1, 2]
            cleaned = re.sub(r',\s*([\]}])', r'\1', cleaned)
            
            # 3. Fix unescaped control characters (like literal newlines in strings)
            # Try to escape literal newlines/tabs between quotes
            def escape_control_chars(match):
                return match.group(0).replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            cleaned = re.sub(r'"[^"]*"', escape_control_chars, cleaned, flags=re.DOTALL)

            try:
                return json.loads(cleaned)
            except json.JSONDecodeError as e2:
                # If still failing, raise the most recent error which might be more descriptive
                raise e2

    def _parse_json_object_at(self, text, json_start):
        depth = 0
        in_string = False
        escape = False
        
        for i in range(json_start, len(text)):
            char = text[i]
            
            if escape:
                escape = False
                continue
            
            if char == '\\':
                escape = True
                continue
            
            if char == '"':
                in_string = not in_string
                continue
            
            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        json_str = text[json_start:i+1]
                        try:
                            return self._relaxed_json_loads(json_str), i + 1
                        except json.JSONDecodeError:
                            return None, i + 1
        return None, None

    def extract_json(self, text, marker):
        """Extracts JSON starting from marker using balanced brace counting."""
        # Case-insensitive search for marker, with or without colon
        pattern = re.compile(re.escape(marker.rstrip(":")), re.IGNORECASE)
        match = pattern.search(text)
        if not match:
            return None
        
        start_idx = match.end()
        json_start = text.find('{', start_idx)
        if json_start == -1:
            # If no { found after marker, try searching before it if the marker is inside the JSON
            # (Gemma 4 sometimes puts the marker as a key)
            json_start = text.rfind('{', 0, match.start())
            if json_start == -1:
                return None

        data, _ = self._parse_json_object_at(text, json_start)
        if data is None:
            print(f"JSON Decode Error for {marker}")
        return data

    def extract_fallback_actions_json(self, text):
        """Accepts exactly one bare or fenced JSON object that looks like ACTIONS_JSON."""
        if not isinstance(text, str):
            return None
        stripped = text.strip()
        candidates = []
        
        # 1. Try fenced blocks
        fence_matches = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        for candidate_text in fence_matches:
            data, _ = self._parse_json_object_at(candidate_text, 0)
            if data is not None:
                candidates.append(data)
        
        # 2. Try searching for any { } if no fenced blocks found
        if not candidates:
            json_start = text.find('{')
            while json_start != -1:
                data, next_start = self._parse_json_object_at(text, json_start)
                if data is not None:
                    candidates.append(data)
                    json_start = text.find('{', next_start)
                else:
                    json_start = text.find('{', json_start + 1)
        
        # Filter for action-shaped objects
        action_candidates = [self._unwrap_actions_json(c) for c in candidates if self._is_action_shaped(self._unwrap_actions_json(c))]
        
        if len(action_candidates) >= 1:
            # Prefer the first one
            return action_candidates[0]
        return None

    def _is_action_shaped(self, data):
        if not isinstance(data, dict):
            return False
        return self.required_action_keys.issubset(data.keys())

    def _unwrap_actions_json(self, data):
        if not isinstance(data, dict):
            return data

        # Explicitly unwrap only allowed wrappers if they contain valid action shapes
        for wrapper_key in ("ACTIONS_JSON", "actions_json"):
            if wrapper_key in data:
                inner = data.get(wrapper_key)
                if self._is_action_shaped(inner):
                    return inner
        
        # If it looks like a wrapped action object but isn't one of the allowed ones, 
        # or if it's already an action-shaped object, return as is (parse() will validate it).
        return data

    def parse(self, text):
        results = {
            "actions": None,
            "writes": [],
            "patches": []
        }
        if not isinstance(text, str):
            return results

        # 1. Primary extraction using marker
        actions = self.extract_json(text, "ACTIONS_JSON:")
        
        # 2. Fallback to bare or fenced JSON
        if actions is None:
            actions = self.extract_fallback_actions_json(text)
        
        # 3. Unwrap if necessary
        actions = self._unwrap_actions_json(actions)
        
        # 4. Strict shape check - reject if it doesn't look like an action object
        if not self._is_action_shaped(actions):
            # If we extracted something but it's not action-shaped, we treat it as None
            # to trigger validation failure/repair.
            actions = None
            
        results["actions"] = actions

        if actions:
            if "writes" in actions:
                results["writes"].extend(actions["writes"])
            if "patches" in actions:
                results["patches"].extend(actions["patches"])

        return results

    def validate_actions(self, actions):
        if not actions:
            return False, "No valid ACTIONS_JSON found or root shape is rejected (e.g. {\"actions\": []})."

        self.normalize_actions(actions)
        
        # Reserved Name Guard: Block shadowing built-in JS/TS objects
        reserved_names = ["Map", "Set", "Object", "Array", "Error", "Date", "Math", "JSON", "Promise"]
        for write in actions.get("writes", []):
            content = write.get("content", "")
            for name in reserved_names:
                # Look for 'class Map', 'interface Map', 'type Map'
                pattern = rf"(class|interface|type)\s+{name}\b"
                if re.search(pattern, content):
                    return False, f"Reserved name conflict: Do not name custom classes/interfaces '{name}' as it shadows built-in JavaScript/TypeScript types. Use a more specific name (e.g., 'World{name}' or 'Game{name}') to avoid typecheck errors."

        if self.validator:
            return self.validator.validate(actions)
            
        # Fallback manual validation
        required_keys = ["stage", "status", "summary"]
        for key in required_keys:
            if key not in actions:
                return False, f"Missing required key in ACTIONS_JSON: {key}"
        
        return True, None

    def normalize_actions(self, actions):
        if not isinstance(actions, dict):
            return actions
            
        if actions.get("qa_result") == "null":
            actions["qa_result"] = None
            
        # Normalize status
        status = actions.get("status")
        if isinstance(status, str):
            status_map = {
                "running": "blocked",
                "in_progress": "blocked",
                "pending": "blocked",
                "working": "blocked",
                "researching": "blocked",
                "success": "complete",
                "done": "complete",
                "finished": "complete",
                "error": "failed"
            }
            lowered = status.lower().strip()
            if lowered in status_map:
                actions["status"] = status_map[lowered]
            
        # Normalize next_stage_recommendation
        allowed_stages = ["concept_producer", "researcher", "designer", "asset_creator", "developer", "qa_tester", "bug_hunter", "debug_dev", "handover_complete"]
        if "next_stage" in actions and "next_stage_recommendation" not in actions:
            actions["next_stage_recommendation"] = actions.get("next_stage")
        actions.pop("next_stage", None)
        rec = actions.get("next_stage_recommendation")
        if rec and rec not in allowed_stages:
            # Map common misspellings or variants
            mapping = {
                "architect": "developer",
                "producer": "concept_producer",
                "test": "qa_tester",
                "qa": "qa_tester",
                "dev": "developer",
                "bug": "bug_hunter"
            }
            actions["next_stage_recommendation"] = mapping.get(rec.lower(), None)

        # Normalize commands
        commands = actions.get("commands", [])
        if isinstance(commands, list):
            new_commands = []
            for command in commands:
                if isinstance(command, str):
                    mapped = self._infer_command_name(command)
                    if mapped:
                        new_commands.append({"name": mapped, "reason": f"Normalized from command string: {command}"})
                    continue
                if not isinstance(command, dict):
                    continue
                name = command.get("name") or command.get("command")
                if not name:
                    continue
                mapped = self._infer_command_name(str(name)) or str(name)
                normalized = {
                    "name": mapped,
                    "reason": str(command.get("reason", "Verification command.")),
                }
                args = command.get("args")
                if isinstance(args, (list, str)) or args is None:
                    normalized["args"] = args
                new_commands.append(normalized)
            actions["commands"] = new_commands

        # Normalize blockers
        blockers = actions.get("blockers", [])
        if isinstance(blockers, list):
            new_blockers = []
            for b in blockers:
                if isinstance(b, str):
                    new_blockers.append({"reason": b})
                elif isinstance(b, dict):
                    if "reason" in b:
                        new_blockers.append({"reason": b["reason"]})
            actions["blockers"] = new_blockers

        # Normalize artifact declarations
        artifacts = actions.get("artifacts", [])
        if isinstance(artifacts, list):
            new_artifacts = []
            for artifact in artifacts:
                if isinstance(artifact, str):
                    name = artifact.replace("\\", "/").rstrip("/").split("/")[-1]
                    if name:
                        new_artifacts.append({"name": name, "type": self._infer_artifact_type(name)})
                    continue
                if not isinstance(artifact, dict):
                    continue
                name = artifact.get("name") or artifact.get("path")
                if not name:
                    continue
                name = str(name).replace("\\", "/").rstrip("/").split("/")[-1]
                if not name:
                    continue
                new_artifacts.append({
                    "name": name,
                    "type": str(artifact.get("type") or self._infer_artifact_type(name))
                })
            actions["artifacts"] = new_artifacts

        # Normalize research_requests
        requests = actions.get("research_requests", [])
        if isinstance(requests, list):
            new_requests = []
            for req in requests:
                if isinstance(req, str):
                    new_requests.append({
                        "query": req,
                        "reason": "Model supplied string research request.",
                        "required": True
                    })
                    continue
                
                if not isinstance(req, dict):
                    continue
                    
                # Handle topic/description -> query
                if "query" not in req and "topic" in req:
                    req["query"] = req.pop("topic")
                if "query" not in req and "description" in req:
                    req["query"] = req["description"]
                
                if "query" not in req:
                    continue # Drop invalid
                    
                # Consolidate reason
                reason = req.get("reason", "")
                for field in ["description", "constraints", "stack"]:
                    if field in req:
                        val = req.pop(field)
                        reason = f"{reason} {field.capitalize()}: {val}".strip()
                req["reason"] = reason or "Required research."
                
                if "required" not in req:
                    req["required"] = True

                if req.get("evidence_type") == "local_codebase":
                    req["mode"] = "local_codebase"
                req.pop("evidence_type", None)

                # 0. Handle model hallucination: stringified dict in query
                # Example: "query": "audit_kind='discovery' target_files=['a.ts']"
                query_str = str(req.get("query", ""))
                if "audit_kind=" in query_str or "target_files=" in query_str:
                    import ast
                    try:
                        # Try to extract keys using regex then parse as literal
                        kind_match = re.search(r"audit_kind=['\"](.*?)['\"]", query_str)
                        if kind_match:
                            req["audit_kind"] = kind_match.group(1)
                        
                        files_match = re.search(r"target_files=\[(.*?)\]", query_str)
                        if files_match:
                            try:
                                files_str = "[" + files_match.group(1) + "]"
                                req["target_files"] = ast.literal_eval(files_str)
                            except:
                                pass
                        
                        # Clean the query to be more natural
                        new_query = re.sub(r"(audit_kind|target_files)=.*?([, ]|$)", "", query_str).strip(", ")
                        if new_query:
                            req["query"] = new_query
                        else:
                            req["query"] = "Local codebase technical audit"
                    except:
                        pass

                target_files = req.get("target_files") or req.get("pruned_context") or []
                if isinstance(target_files, list):
                    req["target_files"] = [str(path) for path in target_files if isinstance(path, str) and path.strip()]
                    if req["target_files"]:
                        req["mode"] = "local_codebase"
                elif target_files is not None:
                    req.pop("target_files", None)

                audit_kind = req.get("audit_kind")
                if audit_kind not in ("discovery", "file_audit"):
                    query_text = str(req.get("query", "")).lower()
                    if "list all files" in query_text or "identify exact paths" in query_text:
                        req["audit_kind"] = "discovery"
                        req["mode"] = "local_codebase"
                    else:
                        req.pop("audit_kind", None)
                elif audit_kind == "discovery":
                    req["mode"] = "local_codebase"

                if req.get("mode") not in ("web", "local_codebase"):
                    req.pop("mode", None)
                    
                # Drop unknown properties (keep only schema properties)
                schema_props = {"query", "reason", "required", "mode", "audit_kind", "target_files"}
                cleaned_req = {k: v for k, v in req.items() if k in schema_props}
                new_requests.append(cleaned_req)
                
            actions["research_requests"] = new_requests
            
        return actions

    def _infer_command_name(self, command_text):
        lowered = command_text.lower().strip()
        if "typecheck" in lowered or "tsc" in lowered:
            return "typecheck"
        if "vitest" in lowered or "npm test" in lowered or lowered == "test":
            return "test"
        if "git status" in lowered:
            return "git_status"
        if "git diff" in lowered:
            return "git_diff"
        if "find_bloat" in lowered:
            return "find_bloat"
        return None

    def _infer_artifact_type(self, name):
        lowered = name.lower()
        if "blueprint" in lowered:
            return "blueprint"
        if "context_map" in lowered or lowered.endswith(".json"):
            return "context_map"
        if "research" in lowered:
            return "research"
        return "file"
