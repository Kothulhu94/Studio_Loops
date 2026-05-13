---
description: Task Template for tracking AI identity contributions
---
# Technical Blueprint: [Feature Name]
**Role:** [Concept Producer / Researcher]
**Status:** [DRAFT / APPROVED / IN-PROGRESS]

---

## 1. Vision (Concept Producer)
*To be defined by the Concept Producer. High-level goal and thematic alignment.*

- **Summary**: [What is this feature?]
- **Thematic Alignment**: [How does it fit the project aesthetic?]
- **Core Loop**: [Describe the player experience]

## 2. Technical Audit (Researcher)
*To be defined by the Researcher. Identifying injection points and risks.*

- **Context Map**: (Reference `.agent/Loop_Flow/context_map.json`)
- **Key Files**:
  - `src/...`
- **System Dependencies**: [What other systems are affected?]
- **Risks & Mitigations**: [Potential blockers or breaking changes]

## 3. Implementation Checklist (Researcher -> Developer)
*To be defined by the Researcher as actionable steps for the Developer.*

- [ ] **Step 1: Scaffolding**
  - [ ] Create `src/...`
  - [ ] Define interfaces in `src/types/...`
- [ ] **Step 2: Core Logic**
  - [ ] Implement ...
- [ ] **Step 3: Integration**
  - [ ] Wire into `src/engine/GameLoop.ts`
- [ ] **Step 4: UI/UX (If applicable)**
  - [ ] Update `src/UI/...`

## 4. Verification (QA Tester)
- [ ] **Test Cases**:
  - [ ] [Test Case 1]
- **Bug Log**: [List found issues]
- **Final Result**: [PASS/FAIL]

---
*This document is the Single Source of Truth for [Feature Name].*

## Output Protocol

- Do not include hidden reasoning or long chain-of-thought.
- Provide concise rationale only when needed for handoff clarity.
- Save durable work into files under `.agent/Loop_Flow/`.
- End every role response with a machine-readable `ACTIONS_JSON` JSON block.
- The orchestrator, not the model, controls role transitions.
