# Studio Loop Local Gemma 4 Harness

This harness runs local Gemma 4 through KoboldCPP.

Primary command:

```bash
python .agent/orchestrator/studio_loop.py auto "Describe task here"
```

Runtime folders:

* `.agent/orchestrator/` - controller and tools
* `.agent/workflows/` - role instructions
* `.agent/skills/` - role skill packs
* `.agent/state/` - active state
* `.agent/Loop_Flow/` - artifacts/context packs
* `.agent/logs/` - model, command, patch, validation logs
* `tools/` - local helper scripts

This project uses local models and a machine-readable JSON protocol at runtime.

## Web Research

The harness performs web research through local browser automation, not paid search APIs.

Primary backend:

- Playwright Chromium

The model does not browse directly. It requests research through `ACTIONS_JSON.research_requests`; the orchestrator performs browser research, extracts page text, writes a research brief, and injects that brief into the next prompt.

No Brave, Tavily, SerpAPI, or paid search account is required.
