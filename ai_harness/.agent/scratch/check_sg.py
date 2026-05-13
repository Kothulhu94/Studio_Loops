import sys
import os

# Add orchestrator path
orchestrator_path = r'c:\Users\rchos\Desktop\Studio_Loop\ai_harness\.agent\orchestrator'
if orchestrator_path not in sys.path:
    sys.path.append(orchestrator_path)

from safety_guard import SafetyGuard

sg = SafetyGuard(orchestrator_path)
print(f"Has is_path_allowed: {hasattr(sg, 'is_path_allowed')}")
print(f"Attributes: {dir(sg)}")
