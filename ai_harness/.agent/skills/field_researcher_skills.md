# Master Skill: Field Researcher Bundle
This consolidated skill file contains all external research capabilities.

---

## 1. Web Research Specialist
**Description**: Gathering external information via search engines and documentation sites.

### Instructions
1. **Define Search Queries**: Break down complex information needs into targeted search queries.
2. **Execute Research**: Use `ACTIONS_JSON.research_requests` with `mode: "web"`.
3. **Information Synthesis**: Compare multiple sources (MDN, GitHub, StackOverflow, etc.) for accuracy.
4. **Tool/Library Scouting**: Identify modern libraries or tools that solve the user's specific problem.
5. **Output**: Generate a "Research Brief" artifact in `.agent/Loop_Flow/`.

### Orchestrator Actions
- **research_requests**: Primary tool. Use `mode: "web"` explicitly.
- **Do not invoke tools directly.**

---

## 2. Competitive & Thematic Research
**Description**: Analyzing existing solutions and thematic references to ensure the project is state-of-the-art.

### Instructions
1. **Thematic Audit**: If the project has a specific theme (e.g., "Solarpunk"), research visual and mechanical tropes associated with it.
2. **Feature Parity**: Research similar features in successful games/apps to identify "must-haves".
3. **Accessibility Standards**: Research modern accessibility patterns for the specific feature.

### Orchestrator Actions
- **research_requests**: Use for external scouting.
