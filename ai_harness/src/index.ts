import { Game, GameState } from './engine/Game';
import { WorldMap } from './world/Map';
import { EntityManager } from './entities/EntityManager';
import { BlueprintLoader } from './engine/BlueprintLoader';

// Mock dependencies for initial setup since they aren't fully defined in context
const mockWorldMap = new WorldMap();
const mockEntityManager = new EntityManager(mockWorldMap);
const mockBlueprintLoader = new BlueprintLoader();

const game = new Game(mockWorldMap, mockEntityManager, mockBlueprintLoader);
window.gameInstance = game; // Expose game instance globally for UI

function initializeGame() {
  console.log("Game initializing...");
  game.setState(GameState.LOADING);
  // Further setup logic
}

initializeGame();