# Master Skill: QA Tester Bundle
This consolidated skill file contains all core capabilities required for the QA Tester identity.

---

## 1. Automated Bug Reproduction
**Description**: Generating `repro.js` scripts in `tools/` that trigger glitches with 100% consistency by injecting specific application states.

### Instructions
1. **Log Analysis**: Review console logs and error traces to understand the state leading to the bug.
2. **State Setup**: Write a script that initializes the application and injects the exact variables required for the bug.
3. **Trigger**: Execute the logical sequence that causes the failure.
4. **Verification**: Confirm that the script fails in the same way as the reported bug.

### Orchestrator Actions
- **Request an allowlisted command through ACTIONS_JSON.commands.**
- **Do not invoke tools directly.**

---

## 2. Performance Bottlenecking
**Description**: Identifying high-frequency functions in the main execution loop that cause performance drops.

### Instructions
1. **Baseline Setup**: Run the application in a stable environment.
2. **Performance Review**: Browser-based performance profiling is currently unavailable. Use unit tests, loop review, and allowlisted analysis commands such as `find_bloat` to identify bottlenecks.
3. **Loop Analysis**: Check the main execution path for unnecessary allocations or heavy calculations.
4. **Report**: Document findings with specific line numbers and execution times.

### Orchestrator Actions
- **Browser visual audit and performance profiling are currently unavailable.** Use research_requests for external research and allowlisted commands only.
- **Request only allowlisted command names through ACTIONS_JSON.commands (e.g., `test`, `test_target`, `typecheck`, `find_bloat`).**
- **Do not invoke tools directly.**

---

## 3. Unit Test Scaffolding
**Description**: Generating Vitest suites for core mathematical logic, utility functions, and system state transitions.

### Instructions
1. **Target Analysis**: Identify pure functions or state-heavy modules needing coverage.
2. **Test Drafting**: Generate test cases for "Happy Path," "Edge Cases," and "Failure Modes."
3. **Mocking Dependencies**: Use Vitest mocks for external systems.
4. **Coverage Audit**: Ensure that critical logic paths have high branch coverage.

### Tools
- `src/__tests__/`: Destination for test files.
- `Vitest`: The test runner.
