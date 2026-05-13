import sys
import os

orchestrator_path = r'c:\Users\rchos\Desktop\Studio_Loop\ai_harness\.agent\orchestrator'
if orchestrator_path not in sys.path:
    sys.path.append(orchestrator_path)

from safety_guard import SafetyGuard

sg = SafetyGuard(orchestrator_path)
# Test calling with all arguments
allowed = sg.is_path_allowed("src/engine/Game.ts", mode="write", stage="developer")
print(f"Is src/engine/Game.ts allowed for developer: {allowed}")
