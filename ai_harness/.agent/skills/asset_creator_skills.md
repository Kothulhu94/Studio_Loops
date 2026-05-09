# Master Skill: Asset Creator Bundle
This consolidated skill file contains all core capabilities required for the Asset Creator identity.

---

## 1. Asset Generation Spec
**Description**: Generating asset specifications that are optimized for creation (clean silhouettes, minimal noise).

### Instructions
1. **Silhouette Focus**: Specify items with clear, distinct silhouettes. Avoid complex backgrounds or soft gradients.
2. **Contrast Enhancement**: Request "black and white ink style," "high-contrast vector style," or "clean stencil" to ensure a sharp threshold for vectorization.
3. **Perspective Consistency**: Ensure assets are specified from a consistent perspective (e.g., flat, side-on, or top-down) as required by the Designer.

### Orchestrator Actions
- **asset_generator capability**: If image generation is available through a configured local or external asset tool, request it through orchestrator capabilities. Otherwise, produce SVG/vector specs, prompt text, and registry integration plans only.

---

## 2. Vectorization Availability
**Description**: Vectorization is unavailable unless a future allowlisted command is added.

### Instructions
1. **Asset Preparation**: Produce SVG specs, filename plans, and registry integration plans only.
2. **No Batch Conversion**: Do not request vectorization commands.
3. **No Registry Edits**: Do not modify source registry files.

### Orchestrator Actions
- **Request only allowlisted command names through ACTIONS_JSON.commands.**
- **Do not invoke tools directly.**

---

## 3. SVG Registry Integration Plan
**Description**: Producing a plan for the Developer to add new SVG assets to the project's central registry files.

### Instructions
1. **ID Selection**: Choose unique, descriptive IDs for each new asset.
2. **Integration Plan**: Document the new SVG paths or raw XML strings in an integration plan artifact for the Developer. Do not modify source registry files.
3. **Verification**: Ensure the integration plan is clear and all assets are documented.

### Orchestrator Actions
- **Request only allowlisted command names through ACTIONS_JSON.commands.**
- **Do not invoke tools directly.**
