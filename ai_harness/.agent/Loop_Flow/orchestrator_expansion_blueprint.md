# Technical Audit

## System Architecture Overview
The system is a multi-agent orchestration framework centered around the `StudioLoopOrchestrator`. It utilizes a graph-based transition engine to move between different agent roles (Designer, Developer, QA, etc.).

### Core Components
- **Orchestrator**: `StudioLoopOrchestrator` manages the lifecycle, state, and transitions.
- **State Management**: `StateStore` maintains the persistent context of the loop.
- **Capability System**: `SkillRegistry` and `CapabilityRegistry` map agent roles to specific executable skills and tools.
- **Execution Layer**: `CommandRunner` and `BrowserBridge` provide the interface for external tool interaction.
- **Context Management**: `ContextPruner` and `ContextCompactor` handle the token window constraints.

### Identified Bottlenecks
- **Context Bloat**: As the loop progresses, the `StateStore` accumulates significant history, requiring aggressive pruning.
- **Skill Discovery**: The mapping between high-level workflow definitions and low-level `skill.json` files is indirect.
- **Error Recovery**: The `RetryEngine` is robust but lacks role-specific recovery logic (e.g., a QA agent should trigger a different recovery than a Developer).

## Implementation Blueprint

### Objective
Enhance the Studio Loop to support more complex, multi-stage autonomous workflows with improved context awareness and error recovery.

### Phase 1: Enhanced Context Management
- **Dynamic Pruning**: Implement a priority-based pruning mechanism in `ContextPruner` that protects 'Critical Path' artifacts (e.g., `skill.json`, `workflow.md`) while discarding transient research logs.
- **Hierarchical State**: Transition `StateStore` to support hierarchical namespaces to prevent key collisions during complex sub-tasks.

### Phase 2: Role-Aware Transition Logic
- **Transition Refinement**: Update `TransitionEngine` to allow roles to suggest 'Sub-Loops' rather than just linear transitions.
- **Recovery Protocols**: Implement `RoleRecoveryHandler` to allow agents to self-correct based on `ResponseParser` errors.

### Phase 3: Tool/Skill Integration
- **Unified Registry**: Consolidate `CapabilityRegistry` and `SkillRegistry` into a single source of truth.

## Context Pruning Map

| Data Type | Retention Policy | Pruning Trigger |
| :--- | :--- | :--- |
| **Core Configs** (.agent/skills/*.json) | Permanent | Never |
| **Workflow Definitions** (.agent/workflows/*.md) | Permanent | Never |
| **Artifacts** (Generated code/assets) | High Priority | Manual/End of Loop |
| **Research Logs** (Browser/Search results) | Low Priority | Token Threshold (70%) |
| **Command Outputs** (Stdout/Stderr) | Medium Priority | Token Threshold (50%) |
| **Agent Thought Process** (Internal Monologue) | Low Priority | Immediate after transition |

## Implementation Checklist
- [ ] Refactor `ContextPruner` to support priority levels.
- [ ] Implement `StateStore` namespacing.
- [ ] Update `TransitionEngine` to support sub-loop branching.
- [ ] Integrate `ResponseParser` error signals into the `RetryEngine`.
- [ ] Standardize skill registration across all agent types.