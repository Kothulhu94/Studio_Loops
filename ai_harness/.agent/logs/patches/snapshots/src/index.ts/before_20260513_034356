import { Game } from './engine/Game';
import { WorldMap } from './world/WorldMap';
import { EntityManager } from './entities/EntityManager';
import { BlueprintLoader } from './BlueprintLoader';

const worldMap = new WorldMap();
const entityManager = new EntityManager();
const blueprintLoader = new BlueprintLoader();
const game = new Game(worldMap, entityManager, blueprintLoader);

// Example usage
game.setState(GameState.LOADING);
console.log(`Game State: ${game.getState()}`);

// Simulate game start
game.startGame();
console.log(`Game Started. Current State: ${game.getState()}`);
