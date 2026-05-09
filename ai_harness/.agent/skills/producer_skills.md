# Master Skill: Concept Producer Bundle
This consolidated skill file contains all core capabilities required for the Concept Producer identity.

---

## 1. Automated ADR Generation
**Description**: Extracting architectural decisions from chat logs and implementation notes into formal `docs/adr/` documentation.

### Instructions
1. **Decision Capture**: Identify a significant architectural choice made during a session (e.g., refactoring a module, choosing a library).
2. **ADR Templating**: Create a new `.md` file in `docs/adr/` using the following format:
   - **Title**: Descriptive name of the decision.
   - **Status**: [Proposed / Accepted / Superseded / Deprecated].
   - **Context**: The problem being solved and the technical constraints.
   - **Decision**: What was decided and why.
   - **Consequences**: What becomes easier or harder as a result.
3. **Linking**: Reference the new ADR in the next `Decision Log` entry to ensure continuity.
4. **Maintenance**: If a decision is changed, update the status of the old ADR and link to the new one.

### Tools
- `docs/adr/`: The repository for these records.
- `Decision Log`: The trigger for identifying new ADR candidates.

---

## 2. AI Architectural Memory
**Description**: Cross-referencing current implementation tasks with past ADRs to prevent "decision drift" and ensure consistency with long-term goals.

### Instructions
1. **ADR Retrieval**: Scan `docs/adr/` for all relevant Architectural Decision Records related to the current module.
2. **Conflict Detection**: Compare the proposed implementation plan with existing decisions.
3. **Alignment Report**: If a conflict is found, flag it to the Researcher or Producer. If aligned, document the specific ADRs that influenced the design.
4. **Memory Update**: Ensure new decisions are captured as ADRs to build the project's long-term architectural memory.

### Tools
- `docs/adr/`: The source of architectural truth.
- `source_indexer`: For finding relevant keywords in ADRs.

---

## 3. System Balance Simulation
**Description**: Running high-speed simulations to identify outliers or edge cases in complex systems.

### Instructions
1. **Simulation Setup**: Define the variables to be randomized and the success criteria.
2. **Simulation Run**: Execute a headless loop of system cycles at high speed.
3. **Data Aggregation**: Collect metrics and identify statistical outliers.
4. **Optimization**: Propose adjustments to the Developer based on simulation results.
