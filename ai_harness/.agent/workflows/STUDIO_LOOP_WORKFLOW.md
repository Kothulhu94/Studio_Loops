---
description: The Studio Loop Workflow utilizing local Gemma 4 orchestration
---
# Studio Loop Workflow

This document defines the official development process for "Studio Loop". It utilizes local Gemma 4 orchestration to ensure every contribution is researched, designed, and verified.

## Running the Studio Loop

Primary command (Autonomous):

```bash
python .agent/orchestrator/studio_loop.py auto "Describe task here"
```

Manual/Step-based commands:

```bash
python .agent/orchestrator/studio_loop.py run "Describe task here"
python .agent/orchestrator/studio_loop.py continue
python .agent/orchestrator/studio_loop.py status
python .agent/orchestrator/studio_loop.py reset
python .agent/orchestrator/studio_loop.py capabilities
```

## Orchestrated Stages

The Studio Loop Orchestrator moves through the following stages automatically:

### 1. Concept Stage (Concept Producer)
*   **Goal**: Define the "What" and "Why".
*   **Action**: Create high-level vision and thematic requirements in `.agent/Loop_Flow/[feature]_blueprint.md`.

### 2. Research & Audit Stage (Researcher)
*   **Goal**: Define technical architecture and implementation steps.
*   **Action**: Evolve the blueprint into a technical audit with injection points and a checklist. Uses the orchestrator-generated source index and context_culler.py output for source analysis.

### 3. Design Stage (Designer)
*   **Goal**: Define UI/UX aesthetics and interaction tokens.
*   **Action**: Generate CSS tokens and component specs in `.agent/Loop_Flow/`.

### 4. Asset Stage (Asset Creator)
*   **Goal**: Generate production-ready assets.
*   **Action**: Produce SVG/vector specs or integrate via orchestrator asset capabilities.

### 5. Implementation Stage (Developer)
*   **Goal**: Write functional, clean code.
*   **Action**: Modify source, tests, and tools. Uses orchestrator `writes` and `patches`.

### 6. Verification Stage (QA Tester)
*   **Goal**: Ensure quality and stability.
*   **Action**: Run tests and perform edge case analysis.

### 7. Forensics Stage (Bug Hunter)
*   **Goal**: Isolate and reproduce reported failures.
*   **Action**: Identify root cause and create reproduction scripts.

### 8. Remediation Stage (Debug Dev)
*   **Goal**: Implement surgical fixes for identified bugs.
*   **Action**: Apply fixes and verify regression.

---

## Best Practices

- **The Debug Loop**: If QA fails, the orchestrator routes to **Bug Hunter** -> **Debug Dev** -> **QA**.
- **Artifact-Driven Handoff**: Every transition is accompanied by updated state and artifacts in `.agent/Loop_Flow/`.
- **Orchestrator Controlled**: The model receives only the active role, task state, artifacts, and pruned context. The model requests actions through `ACTIONS_JSON`.

## Output Protocol

- Do not include hidden reasoning or chain-of-thought.
- Do not use XML cognitive tags.
- Do not claim files were written unless they are listed in `writes`, `patches`, or `artifacts`.
- Do not claim commands were run unless they are listed in `commands`.
- Request all filesystem changes, patches, commands, and research through `ACTIONS_JSON`.
- The orchestrator executes only safe, allowlisted actions.
- End with a valid `ACTIONS_JSON` block.

ACTIONS_JSON:
{
  "stage": "current_stage",
  "status": "complete|blocked|failed",
  "summary": "",
  "design_required": false,
  "assets_required": false,
  "qa_result": null,
  "writes": [],
  "patches": [],
  "commands": [],
  "research_requests": [],
  "artifacts": [],
  "next_stage_recommendation": null,
  "risks": [],
  "blockers": []
}
