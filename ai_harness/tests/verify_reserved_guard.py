import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from response_parser import ResponseParser

def test_reserved_name_guard():
    parser = ResponseParser()
    bad_actions = {
        "stage": "developer",
        "status": "complete",
        "summary": "test",
        "writes": [
            {
                "path": "test.ts",
                "content": "class Map { constructor() {} }"
            }
        ]
    }
    
    valid, error = parser.validate_actions(bad_actions)
    print(f"Valid: {valid}")
    print(f"Error: {error}")
    
    if not valid and "Reserved name conflict" in error:
        print("TEST PASSED: Reserved name was blocked.")
    else:
        print("TEST FAILED: Reserved name was NOT blocked.")

if __name__ == "__main__":
    test_reserved_name_guard()
