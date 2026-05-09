# Master Skill: Researcher Bundle
This consolidated skill file contains all core capabilities required for the Researcher identity.

---

## 1. Architecture Auditor
**Description**: Systematic review of system design, boundaries, data flow, and ADR compliance.

### Instructions
1. **Analyze Requirements**: Review the current feature request against the existing system architecture.
2. **Component Boundaries**: Identify if new components cross existing boundaries or introduce circular dependencies.
3. **Data Flow**: Trace how data enters, moves through, and leaves the new feature.
4. **Scalability**: Evaluate if the proposed solution handles edge cases (e.g., 500,000 troops) efficiently.
5. **ADR Compliance**: Ensure the design adheres to past Architectural Decision Records in `docs/adr/`.
6. **Output**: Generate a "Technical Audit" report following the project's standard format.

### Orchestrator Actions
- **Use the context pack and source index supplied by the orchestrator.**
- **Request an allowlisted command through ACTIONS_JSON.commands.**
- **Do not invoke tools directly.**

---

## 2. Context Pruning & Culling
**Description**: Filtering project context via local scripts to fit massive files into narrow token windows.

### Instructions
1. **Define Scope**: Identify the relevant files for the current task.
2. **Execute Culling**: Use the context pack and source index supplied by the orchestrator. Do not request context_compiler unless it exists in the allowlist.
3. **Map Construction**: Create a "Context Pruning Map" for the Developer/Designer.
4. **Validation**: Ensure no critical dependencies or definitions were pruned out.

### Orchestrator Actions
- **Use the context pack and source index supplied by the orchestrator.**
- **Request an allowlisted command through ACTIONS_JSON.commands.**
- **Do not invoke tools directly.**

---

## 3. Dependency Tree Audit
**Description**: Identifying unused npm packages, version conflicts, and bloated dependencies to maintain a "Flash Drive Friendly" codebase.

### Instructions
1. **Tree Analysis**: Run `npm list` or similar tools to visualize the dependency graph.
2. **Bloat Identification**: Identify large packages that could be replaced by lighter alternatives or vanilla implementations.
3. **Unused Detection**: Check `package.json` against actual imports in the source code to find unused dependencies.
4. **Refactor Recommendation**: Provide a list of packages to prune or consolidate to the Developer.

### Orchestrator Actions
- **package.json**: The manifest.
- **allowlisted command action**: To execute `npm list` or `depcheck`.
- **context_culler / source_indexer**: To verify package usage in source code.

---

## 4. Decision Memory (Architecture)
**Description**: Utilizing the decision logs to perform architectural discovery and maintain consistency.

### Instructions
1. **Deep Search**: Use `source_indexer` on `.agent/logs/` to find past architectural decisions.
2. **Context Seeding**: When starting a major research task, review the `.agent/logs/` to get a "High-Level Architectural Overview".
3. **Decision Logging**: ALWAYS record major research outcomes in `.agent/logs/` using the format: `Decision Log: [Timestamp] [Identity] [Topic] [Outcome]`.
4. **Reporting**: All major findings MUST be saved as a `.md` report in `.agent/Loop_Flow/`.

### Orchestrator Actions
- **.agent/logs/**: The architectural memory storage.

---

## 5. Semantic Sight (LSP)
**Description**: Deep symbolic indexing and type-aware navigation via Language Server Protocol.

### Instructions
1. **Symbol Search**: Use available orchestrator LSP capabilities to find all definitions, references, and implementations of a symbol.
2. **Type Inspection**: Use available orchestrator LSP capabilities to see full type signatures.
3. **Workspace Diagnostics**: Scan the entire project for hidden type errors that `tsc` might miss in incremental mode.
4. **Integration**: If LSP is unavailable, fall back to `context_culler / source_indexer` and `context pack / source index` with manual type deduction.

### Orchestrator Actions
- **Use the context pack and source index supplied by the orchestrator.**
- **Do not invoke tools directly.**

---

## 6. Memory Leak Forensics
**Description**: Analyzing JavaScript heap snapshots and allocation timelines to identify retained objects in long-duration game sessions.

### Instructions
1. **Baseline Capture**: Record a heap snapshot after the game finishes loading but before significant action.
2. **Stress Session**: Perform high-frequency actions (combat, menu cycling, area transitions) for 10-15 minutes.
3. **Comparison**: Capture a second snapshot and compare with the baseline to find objects that were not garbage collected.
4. **Root Cause**: Trace the retainer path of leaked objects (e.g., event listeners not removed, global array growth).

### Orchestrator Actions
- Browser audit is not currently available. Do not request browser_audit. Use research_requests for external research and allowlisted commands only.
- **Request an allowlisted command through ACTIONS_JSON.commands.**
- **Do not invoke tools directly.**
