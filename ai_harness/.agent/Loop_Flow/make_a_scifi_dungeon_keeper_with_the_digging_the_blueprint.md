# Technical Blueprint: Sci-fi Terraforming Keeper

## 1. Technical Audit

**Scope Assessment:** The feature requires a massive, single, expanding map, which is the primary technical challenge. The concept successfully replaces subterranean digging with surface terraforming/cutting through hostile flora. The core loop (Expansion $\leftrightarrow$ Threat $\leftrightarrow$ Economy) is sound for a management/strategy game.

**Architectural Fit:** The game logic must be implemented in TypeScript/Vanilla JS, targeting the Browser/DOM environment. The map structure must be highly optimized for sparse data representation to handle an 'expanding' map without memory exhaustion.

**Component Boundaries:**
*   **Map System:** Needs to be the central, most complex component, handling procedural generation, state persistence, and boundary expansion.
*   **Entity System:** Must manage diverse entities (Player structures, Troops, Alien Fauna, Flora) and their interactions with the map state.
*   **Economy/Simulation:** Requires a discrete time-step simulation loop to balance resource generation against upkeep and threat progression.

**Scalability Concerns:**
1.  **Map Size:** A dense grid structure will fail quickly. Sparse data structures (e.g., HashMaps or Quadtrees) are mandatory for efficient lookups and rendering of only 'active' or 'explored' cells.
2.  **Simulation Load:** The economic and combat simulation must be optimized to run efficiently within the browser's main thread or offloaded to Web Workers.

**Dependencies:** The core relies heavily on efficient data structures (Map/Set/Custom Grid implementation) and DOM/Canvas rendering capabilities.

## 2. Implementation Blueprint

### A. Core Systems

1.  **Map Generation & Management (`Map.ts`):**
    *   Implement a sparse grid structure (e.g., using a `Map<string, CellData>` where the key is a coordinate string like "x,y").
    *   Define `CellData` to hold terrain type (Vines, Biomass, Clear, Mineral Deposit, Habitable Zone).
    *   Implement a controlled expansion mechanism: When the player attempts to interact with an unmapped boundary, the system generates and registers new adjacent cells based on procedural rules.
    *   Implement pathfinding/clearing logic that modifies the cell state from 'Vines' to 'Clear' or 'Habitable'.
2.  **Entity Management (`EntityManager.ts`):**
    *   Define base classes for `Unit`, `Structure`, and `Threat`. All must reference their location on the Map.
    *   Implement AI for Alien Fauna: Simple state machines reacting to player encroachment (e.g., patrol, attack, retreat).
    *   Implement Player Actions: Troop deployment, Spell casting (which modifies cell state/applies buffs), and Habitat construction.
3.  **Simulation & Economy (`Game.ts`):**
    *   Implement a main game loop (e.g., using `requestAnimationFrame` or a fixed-timestep loop). 
    *   **Resource Cycle:** Resources are generated based on cell type/presence of structures. Upkeep is calculated based on deployed troops/structures.
    *   **Threat Progression:** Alien biomass/threat level increases over time unless actively countered by terraforming efforts.

### B. Sci-Fi Thematic Mapping

*   **Digging $\rightarrow$ Terraforming Pulse:** Player action to clear vines/brambles, consuming Energy and Biomass to convert terrain state.
*   **Rooms $\rightarrow$ Habitats/Bio-Domes:** Structures that provide resource processing or troop housing.
*   **Troops $\rightarrow$ Bio-Engineers/Defense Drones:** Units specialized in clearing, harvesting, or combat.
*   **Traps $\rightarrow$ Environmental Inhibitors:** Automated systems that alter local terrain or disrupt alien growth.
*   **Spells $\rightarrow$ Terraforming Pulses/Energy Projection:** High-cost actions that apply temporary or permanent state changes to cells.
*   **Enemies $\rightarrow$ Xenofauna & Aggressive Flora:** The planet's native defense mechanisms.

## 3. Context Pruning Map

This map is designed to provide the Developer with the necessary architectural context without overwhelming the token limit, focusing on the core data structures and interfaces.

```json
{
  "files": [
    {
      "path": "src/world/Map.ts",
      "lines": "1-18",
      "reason": "Defines the core sparse grid structure and cell data types."
    },
    {
      "path": "src/entities/EntityManager.ts",
      "lines": "12-23",
      "reason": "Defines entity interfaces and location management."
    },
    {
      "path": "src/engine/Game.ts",
      "lines": "1-20",
      "reason": "Defines the main game loop and simulation entry point."
    },
    {
      "path": "src/index.ts",
      "lines": "1-6",
      "reason": "Entry point and initialization logic."
    },
    {
      "path": "tests/test_local_codebase_audit.py",
      "lines": "307-326",
      "reason": "To understand existing testing patterns for local code structure."
    }
  ],
  "reason": "Focusing on the core data models (Map, Entity, Game) and minimal setup code to begin implementation of the sparse grid and simulation loop."
}
```

## 4. Implementation Checklist

[ ] **[Architecture]** Define the `CellData` interface/type for the sparse map, including terrain type, resource presence, and threat level.
[ ] **[Map System]** Implement the `Map` class using a JavaScript `Map` object for sparse coordinate storage (e.g., key: "x,y").
[ ] **[Map System]** Implement the boundary expansion logic: generating new, default terrain cells when accessed outside the current map bounds.
[ ] **[Entity System]** Define base classes/interfaces for `Unit`, `Structure`, and `Threat`.
[ ] **[Entity System]** Implement location tracking for all entities relative to the Map coordinates.
[ ] **[Simulation]** Implement the discrete time-step loop in `Game.ts`.
[ ] **[Simulation]** Implement basic resource generation logic based on cell type.
[ ] **[Simulation]** Implement basic threat progression logic (e.g., threat increases by X per tick if not countered).
[ ] **[Thematic]** Implement the 'Clear Path' action: A function that consumes resources and changes a cell's state from 'Vines' to 'Clear'.
[ ] **[Thematic]** Implement the 'Terraforming Pulse' action: A function that applies a state change (e.g., 'Vines' $\rightarrow$ 'Habitable') to a target cell.
[ ] **[Rendering]** (Future Stage) Integrate Canvas/DOM drawing to visualize the map state.
[ ] **[Testing]** Write unit tests for the map expansion and state mutation functions using Vitest.
