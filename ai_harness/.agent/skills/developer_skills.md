# Master Skill: Developer Bundle
This consolidated skill file contains all core capabilities required for the Developer identity.

---

## 1. AST-Aware Refactoring
**Description**: Precise code modification using abstract syntax tree manipulation to avoid syntax errors.

### Instructions
1. **Target Identification**: Identify the symbols or structures needing refactoring.
2. **Context Gathering**: Use `context pack / source index` to understand all references.
3. **Refactor Plan**: Draft the changes focusing on type safety and symbol consistency.
4. **Verification**: Always run `typecheck` after refactoring to ensure no regressions occurred.

### Orchestrator Actions
- **typecheck**: Verification.
- **context pack / source index**: Context.

---

## 2. Data-Driven Templating
**Description**: Converting raw data tables (CSV/JSON) into strictly-typed TypeScript classes and registry entries.

### Instructions
1. **Data Parsing**: Implement loaders for raw project data.
2. **Type Generation**: Create interfaces that match the data schema.
3. **Registry Pattern**: Automatically register entities into central lookup systems during initialization.
4. **Validation**: Add runtime checks to ensure that data errors are caught during the load phase.

---

## 3. Save Game / State Schema Migration
**Description**: Automating versioned upgrades for the application's state JSON to prevent broken states after structural changes.

### Instructions
1. **Schema Versioning**: Ensure every state file contains a `version` field.
2. **Transformer Creation**: Write pure functions that map data from Version N to Version N+1.
3. **Regression Testing**: Use past state samples to verify that the migration logic preserves data.

---

## 4. TypeScript Type Integrity
**Description**: Proactively strengthening interfaces, eliminating `any` types, and ensuring strict null checks.

### Instructions
1. **Any Hunting**: Search the codebase for `any` or `unknown` types that can be replaced with specific interfaces.
2. **Interface Hardening**: Review existing interfaces to ensure they accurately reflect runtime data.
3. **Strict Check Compliance**: Verify that new code handles null/undefined cases correctly.

---

## 5. Stateful Orchestration
**Description**: Managing autonomous transitions between Concept Producer, Researcher, Designer, and Developer stages.

### Instructions
1. **State Tracking**: Monitor the current phase of the Studio Loop (Concept -> Research -> Design -> Implementation -> Verification).
2. **Artifact Verification**: Before transitioning, ensure the required artifact for the current stage exists in `.agent/Loop_Flow/`.
3. **Stage Activation**: The orchestrator activates the next role and supplies the required context pack.
4. **Flow Persistence**: Maintain a record of the feature's progression to prevent redundant work or missing steps.

### Orchestrator Actions
- **.agent/Loop_Flow/**: Storage for hand-off artifacts.
- **studio_loop_state.json**: Verification of data integrity between stages.
## 6. Incremental Implementation
**Description**: Breaking down complex scaffolds into manageable, verified steps to ensure system stability.

### Instructions
1. **Incremental but Autonomous**: While you should focus on logic in manageable chunks, use `status: running` to automatically trigger the next turn for verification and subsequent implementation steps. 
2. **Avoid Premature Blocks**: Do not use `status: blocked` for normal step-by-step progress. Only use it if you are truly stuck or need user clarification.
3. **Continuous Verification**: Always include `commands: ["typecheck"]` (or similar) in your ACTIONS_JSON. If it passes, set `status: running` to proceed to the next task in the blueprint.
4. **Context Maintenance**: Keep implementation summaries detailed so the next turn has clear continuity.

---

## 7. Implementation Mandate
**Description**: Ensuring that the development stage does not terminate until all tasks in the Feature Blueprint are addressed.

### Instructions
1. **Blueprint Audit**: Before marking a stage as `complete`, you MUST audit the `feature_blueprint.md` or implementation plan in `.agent/Loop_Flow/`.
2. **Action Requirement**: If the blueprint defines files to be created or logic to be implemented, and those files do not exist or logic is missing, you MUST NOT set `status: complete`.
3. **Avoid Premature Handover**: Do not recommend a transition to `qa_tester` if you have not performed at least one `write` or `patch` action that addresses the feature requirements.
4. **Task Progress**: Use the `summary` field to explicitly list which blueprint tasks were completed and which are pending for the next turn.
