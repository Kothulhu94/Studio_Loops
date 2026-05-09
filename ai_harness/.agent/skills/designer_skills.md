# Master Skill: Designer Bundle
This consolidated skill file contains all core capabilities required for the Designer identity.

---

## 1. Modern Aesthetic Sync
**Description**: Ensuring all new assets, UI components, and shaders adhere to a premium, modern visual identity.

### Instructions
1. **Color Palette Enforcement**: Use curated, harmonious color palettes (e.g., sleek dark modes, vibrant accent colors).
2. **Material Standards**: Apply modern UI effects like "Glassmorphism" (blur + transparency) and high-quality shadows.
3. **Micro-animations**: Add subtle "pulsing" or "breathing" animations to interactive elements.
4. **Visual Audit**: Browser visual audit is currently unavailable. Produce design specs and manual QA checklists for CSS/token criteria only.

### Orchestrator Actions
- **index.css**: The root of the design system.

---

## 2. UI Color Contrast Auditing
**Description**: Automatically checking UI palettes against WCAG standards to ensure high accessibility and legibility.

### Instructions
1. **Palette Sampling**: Identify the background and foreground colors used in a UI component.
2. **Contrast Calculation**: Use WCAG formulas to determine the contrast ratio.
3. **Accessibility Pass**: Ensure a minimum ratio of 4.5:1 for normal text and 3:1 for large text.
4. **Remediation**: Adjust the luminosity or saturation of colors if they fail the audit.

### Orchestrator Actions
- **Browser visual audit is currently unavailable.** Use manual contrast checks or design tool verification.
- **WCAG Guidelines**: The standard for compliance.

---

## 3. Visual Regression Testing
**Description**: Using browser capabilities to compare UI screenshots across different build states to prevent "UI Drift."

### Instructions
1. **Baseline Generation**: Capture "Golden Master" screenshots of key UI states (Main Menu, HUD, Settings).
2. **Build Comparison**: Run the same sequence on the new build and capture matching screenshots.
3. **Difference Analysis**: Identify pixel-level differences or layout shifts.
4. **Report**: Categorize changes as "Intended" (Design Update) or "Regressions" (Bugs).

### Orchestrator Actions
- **Browser visual audit is currently unavailable.** Producing design specs and testable CSS criteria only. Do not request browser screenshots.

---

## 4. WebGPU Shader Synthesis
**Description**: Converting high-level logic into optimized WGSL (WebGPU Shading Language) for GPU-side rendering and simulation.

### Instructions
1. **Logic Analysis**: Identify the mathematical logic to be offloaded to the GPU.
2. **WGSL Generation**: Draft the shader code focusing on data alignment and performance.
3. **Host-Side Binding**: Define the bind groups and pipeline layouts in TypeScript.
4. **Optimization**: Audit the shader for branching overhead.

### Orchestrator Actions
- **src/renderer/shaders/**: Destination for WGSL files.
- **WebGPU API**: For implementation.
