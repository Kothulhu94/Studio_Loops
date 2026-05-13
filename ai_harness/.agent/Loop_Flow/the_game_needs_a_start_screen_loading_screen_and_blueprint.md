# Technical Audit

## Current State Analysis
The existing architecture focuses on agentic orchestration, state management (`StateStore`), and skill execution (`SkillRegistry`). There is currently no defined UI/UX lifecycle or asset-loading pipeline for the game client itself.

## Gap Analysis
1. **Lifecycle Gap**: No transition state between 'Engine Initialization' and 'Game Loop'.
2. **Asset Pipeline Gap**: No mechanism to track asset readiness during a loading phase.
3. **Data Gap**: Lack of a 'Blueprint' schema to define scene configurations, UI layouts, and initial game states.

## Technical Risks
- **State Desync**: The `StateStore` must be synchronized with the UI state to prevent 'ghost' inputs during loading.
- **Blocking I/O**: Loading screens must run on a separate thread/process from the asset deserialization to prevent UI freezing.

# Implementation Blueprint

## 1. The Blueprint System
- **Definition**: A JSON-based schema defining `SceneID`, `RequiredAssets[]`, `InitialState`, and `UIOverlayConfig`.
- **Registry**: A `BlueprintRegistry` service to fetch and validate these definitions.

## 2. Loading Screen Architecture
- **Phase 1: Pre-load**: Fetch Blueprint $\rightarrow$ Parse dependencies.
- **Phase 2: Async Load**: Execute `AssetLoader` tasks while updating a `Progress` float (0.0-1.0).
- **Phase 3: Handshake**: Verify all assets are in memory $\rightarrow$ Signal `TransitionEngine`.

## 3. Start Screen Implementation
- **State**: `GAME_STATE_MENU`.
- **Components**: Title, Play Button, Settings, Credits.
- **Input**: Capture initial user intent (e.g., 'Start Game') to trigger the next Blueprint load.

# Context Pruning Map

To implement this without bloating the agentic orchestrator, we will prune the following context:
- **Exclude from Agent Context**: Low-level shader code, individual texture byte-data, and specific UI widget implementation details.
- **Include in Agent Context**: Blueprint schemas, Loading State transitions, and Asset Manifest structures.
- **Pruning Strategy**: Use a 'Manifest-First' approach where the agent only sees the *description* of assets, not the assets themselves.

# Implementation Checklist

- [ ] **Core**: Define `Blueprint` JSON Schema.
- [ ] **Core**: Implement `BlueprintLoader` service.
- [ ] **UI**: Create `LoadingScreen` component with progress bar.
- [ ] **UI**: Create `StartScreen` component with menu navigation.
- [ ] **System**: Integrate `LoadingState` into the main `TransitionEngine`.
- [ ] **Test**: Verify 'Loading $\rightarrow$ Start Screen $\rightarrow$ Game' flow.