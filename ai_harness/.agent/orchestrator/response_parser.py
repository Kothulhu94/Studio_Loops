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

    def extract_json(self, text, marker):
        """Extracts JSON starting from marker using balanced brace counting."""
        start_idx = text.find(marker)
        if start_idx == -1:
            return None
        
        json_start = text.find('{', start_idx)
        if json_start == -1:
            return None
        
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
                            return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            print(f"JSON Decode Error for {marker}: {e}")
                            return None
        return None

    def parse(self, text):
        results = {
            "actions": None,
            "writes": [],
            "patches": []
        }

        # Extract ACTIONS_JSON using balanced braces
        actions = self.extract_json(text, "ACTIONS_JSON:")
        results["actions"] = actions

        if actions:
            if "writes" in actions:
                results["writes"].extend(actions["writes"])
            if "patches" in actions:
                results["patches"].extend(actions["patches"])

        return results

    def validate_actions(self, actions):
        if not actions:
            return False, "No valid ACTIONS_JSON found."
        
        if self.validator:
            return self.validator.validate(actions)
            
        # Fallback manual validation
        required_keys = ["stage", "status", "summary"]
        for key in required_keys:
            if key not in actions:
                return False, f"Missing required key in ACTIONS_JSON: {key}"
        
        return True, None
