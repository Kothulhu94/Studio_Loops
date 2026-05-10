# Technical Audit

## Current State Analysis
The Studio Loop harness currently relies on a direct orchestration model where the `StudioLoopOrchestrator` transitions between roles based on the `TransitionEngine`. While functional, the system lacks a formal 'Safety Gate' between the `ResponseParser` and the `CommandRunner`.

### Identified Vulnerabilities:
1. **Unvalidated Command Execution**: The `CommandRunner` executes commands derived from LLM outputs with minimal semantic validation, posing a risk of accidental system-level destructive actions.
2. **Contextual Drift**: As the loop progresses, the `ContextCompactor` and `ContextPruner` manage history, but there is no guarantee of 'semantic integrity'—essential state information can be pruned to make room for transient research data.
3. **Role-Permission Mismatch**: Roles defined in `.agent/workflows/` do not have hard-coded capability constraints enforced at the orchestrator level.

## Implementation Blueprint

### Phase 1: The Safety Gate (Pre-Flight Validation)
Introduce a `SafetyGate` component between `ResponseParser` and `CommandRunner`. 
- **Command Whitelisting**: Implement a regex and semantic check for `CommandRunner` arguments.
- **Risk Scoring**: Assign a risk score to every command (e.g., `ls` = 0, `rm` = 10, `git push` = 5). Commands exceeding a threshold require a 'Human-in-the-loop' or a 'High-Confidence' verification step.

### Phase 2: Semantic Context Management
Upgrade `ContextPruner` to use a 'Semantic Importance' heuristic.
- **Pinned Context**: Allow the orchestrator to 'pin' specific metadata (e.g., current task goal, active file paths) so they are never pruned.
- **Tiered Summarization**: Instead of simple pruning, implement tiered summarization where older context is compressed into high-level summaries rather than being deleted.

### Phase 3: Capability-Bound Roles
Integrate `CapabilityRegistry` directly into the `TransitionEngine`.
- When a role transition occurs, the `TransitionEngine` must verify that the new role's `CapabilityRegistry` permits the pending commands in the queue.

## Context Pruning Map

| Context Type | Retention Strategy | Pruning Trigger |
| :--- | :--- | :--- |
| **Task Goal/Instruction** | Pinned (Never Prune) | N/A |
| **Active File Content** | High Priority (Summarize if > 50% window) | Token Limit > 70% |
| **Tool Outputs (Raw)** | Low Priority (Prune after 3 turns) | Token Limit > 80% |
| **Agent Reasoning/Thought** | Medium Priority (Summarize into 'History') | Token Limit > 60% |
| **Error Logs** | High Priority (Keep until resolved) | Error Resolution Event |

## Implementation Checklist

- [ ] **Core**: Implement `SafetyGate` class in `.agent/orchestrator/`.
- [ ] **Core**: Update `CommandRunner` to accept `SafetyGate` validation results.
- [ ] **Context**: Modify `ContextPruner` to support 'Pinned' keys.
- [ ] **Testing**: Add unit tests in `tests/test_safety_gate.py`.
- [ ] **Integration**: Update `StudioLoopOrchestrator` to include the pre-flight check in the main loop.