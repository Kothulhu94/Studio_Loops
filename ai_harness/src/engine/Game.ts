import { WorldMap } from '../world/Map';
import { EntityManager } from '../entities/EntityManager';
import { BlueprintLoader } from './BlueprintLoader';

export enum GameState {
  LOADING = 'LOADING',
  ENTRY_SEQUENCE = 'ENTRY_SEQUENCE',
  MAIN_MENU = 'MAIN_MENU',
  GAMEPLAY = 'GAMEPLAY'
}

export class Game {
  private state: GameState = GameState.LOADING;
  private worldMap: WorldMap;
  private entityManager: EntityManager;
  private blueprintLoader: BlueprintLoader;
  private stateChangeListeners: ((newState: GameState) => void)[] = [];

  constructor(worldMap: WorldMap) {
    this.worldMap = worldMap;
    this.entityManager = new EntityManager(this.worldMap);
    this.blueprintLoader = new BlueprintLoader();
  }

  public getState(): GameState {
    return this.state;
  }

  public setState(newState: GameState): void {
    if (this.state === newState) return;
    this.state = newState;
    console.log(`[Game] State transitioned to: ${newState}`);
    this.notifyStateChange(newState);
  }

  public onStateChange(listener: (newState: GameState) => void): void {
    this.stateChangeListeners.push(listener);
  }

  private notifyStateChange(newState: GameState): void {
    for (const listener of this.stateChangeListeners) {
      listener(newState);
    }
  }

  public getEntityManager(): EntityManager {
    return this.entityManager;
  }

  public startGame(): void {
    console.log('[Game] Starting simulation...');
    
    // Initial state logic
    this.setState(GameState.LOADING);

    // Simulate asset loading completion after a short delay
    setTimeout(() => {
      this.setState(GameState.ENTRY_SEQUENCE);
    }, 1500);
  }

  public stopGame(): void {
    console.log('[Game] Stopping simulation...');
  }
}