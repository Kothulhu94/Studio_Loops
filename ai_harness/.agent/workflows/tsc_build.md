---
description: pre git trial build
---

%~d0\PortableApps\Node\node-v24.15.0-win-x64\node.exe node_modules\typescript\bin\tsc --noEmit
## Output Protocol

- Do not include hidden reasoning or long chain-of-thought.
- Provide concise rationale only when needed for handoff clarity.
- Save durable work into files under `.agent/Loop_Flow/`.
- End every role response with a machine-readable `ACTIONS_JSON` JSON block.
- The orchestrator, not the model, controls role transitions.
