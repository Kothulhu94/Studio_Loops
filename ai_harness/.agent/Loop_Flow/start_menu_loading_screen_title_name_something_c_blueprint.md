# Technical Blueprint: Entry Sequence (Title, Loading, Menu)

## Technical Audit
- **State Integration**: The current `GameState` in `src/engine/Game.ts` needs an expansion to include `ENTRY_SEQUENCE` (covering Title/Loading) and `MAIN_MENU`. 
- **DOM vs Canvas**: The menu and loading text should be implemented using DOM elements overlaid on the Canvas. This allows for easier CSS-based scanline/flicker effects and better accessibility for text-heavy terminal interfaces.
- **Dependency Check**: No new npm packages are required; vanilla CSS and TypeScript are sufficient for the 'Low-Fi' aesthetic.
- **Risk**: Ensuring the transition from the 'Loading' state to the 'Menu' state is seamless and doesn't cause a frame drop that breaks the 'glitch' immersion.

## Implementation Blueprint

### 1. Visual Layer (CSS/DOM)
- **Scanline Overlay**: A fixed `div` with a repeating `linear-gradient` to simulate CRT lines.
- **Flicker Effect**: A global `@keyframes` animation applying subtle opacity shifts (0.97 to 1.0) to the entire UI container.
- **Typography**: Use a monospace font stack (e.g., `'Courier New', monospace`).

### 2. State Machine Logic
- **Phase 1: Initialization**: `src/index.ts` triggers `initializeGame()`. The engine enters `GameState.LOADING`.
- **Phase 2: Asset Reconstitution**: The `LoadingScreen` component listens to `BlueprintLoader` progress. Text updates dynamically (e.g., "Deciphering packets... [45%]").
- **Phase 3: Menu Activation**: Once assets are ready, transition to `GameState.MAIN_MENU`. The DOM renders the terminal-style menu options.

### 3. Component Structure
- `EntrySequenceManager.ts`: Orchestrates the visibility of the UI layers.
- `TerminalUI.ts`: Handles the text-typing effect and menu selection logic.

## Context Pruning Map
To implement this, the Developer needs:
- `src/engine/Game.ts`: To modify `GameState` and the main loop.
- `src/index.ts`: To hook into the initial startup sequence.
- `ui/index.html`: To add the UI container/overlay elements.
- `ui/style.css`: To add the CRT/Scanline/Flicker styles.
- `ui/app.js`: To implement the DOM-based menu logic.

## Implementation Checklist
- [ ] Update `GameState` enum in `src/engine/Game.ts`.
- [ ] Add CSS scanline and flicker keyframes to `ui/style.css`.
- [ ] Create `ui/overlay.html` or update `ui/index.html` with a `#ui-layer` container.
- [ ] Implement `LoadingScreen` logic that reads progress from `BlueprintLoader`.
- [ ] Implement `MainMenu` logic with keyboard/click support for `[INITIALIZE_LINK]`.
- [ ] Verify state transitions from `LOADING` -> `MENU` -> `GAMEPLAY`.