/**
 * @fileoverview Entry point for the game simulation.
 */

import { WorldMap } from './world/Map';
import { Game } from './engine/Game';
import { EntityManager } from './entities/EntityManager';

function initializeGame(): void {
    console.log("--- Initializing Game Engine ---");

    // 1. Initialize World Map
    const worldMap = new WorldMap();
    
    // Seed the map with some initial terrain
    worldMap.setTerrain(0, 0, 'HabitableZone');
    worldMap.setTerrain(1, 0, 'Vines');

    // 2. Initialize Game Engine
    const game = new Game(worldMap);

    // 3. Initialize Entities
    const entityManager = game.getEntityManager();
    const player = entityManager.createEntity('Player', { x: 0, y: 0 });
    const resourceNode = entityManager.createEntity('Resource', { x: 5, y: 5 });
    
    console.log(`Entities created: ${entityManager.getAllEntities().length}`);

    // 4. Start Simulation
    game.startGame();

    // 5. Expose globally for the UI layer
    (window as any).gameInstance = game;

    // In a real application, you would handle window closing/events to call game.stopGame()
}

// Start the application
initializeGame();

