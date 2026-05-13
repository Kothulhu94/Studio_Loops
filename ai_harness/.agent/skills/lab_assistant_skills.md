# Master Skill: Lab Assistant Bundle
This consolidated skill file contains all internal project auditing and context management capabilities.

---

## 1. Architecture Auditor
**Description**: Systematic review of system design, boundaries, data flow, and ADR compliance.

### Instructions
1. **Analyze Requirements**: Review the current feature request against the existing system architecture.
2. **Component Boundaries**: Identify if new components cross existing boundaries or introduce circular dependencies.
3. **Data Flow**: Trace how data enters, moves through, and leaves the new feature.
4. **ADR Compliance**: Ensure the design adheres to past Architectural Decision Records in `docs/adr/`.
5. **Output**: Generate a "Technical Audit" report following the project's standard format.

### Orchestrator Actions
- **research_requests**: Use `mode: "local_codebase"` or `audit_kind: "discovery"`.

---

## 2. Context Pruning & Culling
**Description**: Filtering project context to fit massive files into narrow token windows.

### Instructions
1. **Define Scope**: Identify the relevant files for the current task.
2. **Map Construction**: Create a "Context Pruning Map" for the Developer/Designer.
3. **Validation**: Ensure no critical dependencies or definitions were pruned out.

### Orchestrator Actions
- **file_writer**: To save `context_map.json`.

---

## 3. Dependency Tree Audit
**Description**: Identifying unused npm packages, version conflicts, and bloated dependencies.

### Instructions
1. **Tree Analysis**: Use allowlisted commands to visualize the dependency graph.
2. **Bloat Identification**: Identify large packages that could be replaced by lighter alternatives.

### Orchestrator Actions
- **commands**: Use `find_bloat`.

---

## 4. Semantic Sight (LSP)
**Description**: Deep symbolic indexing and type-aware navigation.

### Instructions
1. **Symbol Search**: Find all definitions, references, and implementations of a symbol.
2. **Type Inspection**: See full type signatures.

---

## 5. Memory Leak Forensics
**Description**: Analyzing source code for potential memory leaks in long-duration game sessions.

### Instructions
1. **Static Review**: Inspect allocation-heavy loops and event listener lifecycles.
2. **Root Cause**: Document likely retention paths.
