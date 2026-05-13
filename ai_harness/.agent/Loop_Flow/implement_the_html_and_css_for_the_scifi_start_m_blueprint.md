# Technical Blueprint: Sci-Fi Start Menu & Loading Screen

## Technical Audit
- **State Synchronization**: The engine uses a `GameState` enum in `src/engine/Game.ts`. The UI must not poll; instead, a `UIController` should subscribe to state changes or be notified by the `Game` class to minimize CPU overhead.
- **DOM Architecture**: To prevent layout thrashing, the UI should be managed as a single overlay container in `public/index.html` with sub-containers for `loading-screen`, `entry-sequence`, and `main-menu`.
- **Performance**: Use `transform` and `opacity` for animations to ensure they are handled by the GPU (compositor thread) rather than triggering layout/reflow.
- **Dependency Check**: No new npm packages are required; vanilla DOM APIs and TypeScript are sufficient.

## Implementation Blueprint

### 1. HTML Structure (`public/index.html`)
- A `#ui-overlay` container.
- `#loading-screen`: Progress bar, status text, and scanline overlay.
- `#entry-sequence`: Cinematic text/logo fade-ins.
- `#main-menu`: Title, 'Start Game' button, 'Options', and 'Exit'.

### 2. CSS Strategy (`public/style.css`)
- **Theme**: Dark background (`#050505`) with neon accents (Cyan: `#00f2ff`, Amber: `#ffb300`).
- **Animations**: 
  - `glitch`: Subtle text jitter using `clip-path`.
  - `pulse`: Breathing effect for menu buttons.
  - `scanline`: A moving linear-gradient overlay to simulate a CRT monitor.
- **Transitions**: Use `opacity` and `visibility` for state transitions between screens.

### 3. TypeScript Bridge (`src/ui/UIManager.ts` - New File)
- **Class `UIManager`**: 
  - Holds references to DOM elements.
  - Method `update(state: GameState)`: Uses a `switch` statement to toggle visibility of UI containers.
  - Method `setLoadingProgress(percent: number)`: Updates the loading bar width.
- **Integration**: The `Game` class should call `uiManager.update(this.state)` during its update loop or state transition.

## Context Pruning Map
{
  "files": [
    {
      "path": "src/engine/Game.ts",
      "ranges": ["L1-L65"], 
      "reason": "To understand GameState enum and the Game class structure."
    },
    {
      "path": "public/index.html",
      "ranges": ["L1-L150"], 
      "reason": "To identify the injection point for the UI overlay."
    },
    {
      "path": "public/style.css",
      "ranges": ["L1-L200"], 
      "reason": "To integrate new sci-fi styles without duplication."
    }
  ]
}

## Implementation Checklist
- [ ] Create `#ui-overlay` and sub-containers in `public/index.html`.
- [ ] Implement CSS variables for sci-fi color palette in `public/style.css`.
- [ ] Add `@keyframes` for `scanline` and `glitch` effects.
- [ ] Implement `UIManager.ts` to handle `GameState` transitions.
- [ ] Connect `Game.ts` to `UIManager` via a state-change notification.
- [ ] Verify transition `LOADING -> ENTRY_SEQUENCE -> MAIN_MENU` works in browser.
- [ ] Write Vitest test to ensure `UIManager` correctly toggles DOM visibility based on `GameState`.