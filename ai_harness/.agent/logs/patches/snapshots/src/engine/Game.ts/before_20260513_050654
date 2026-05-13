import { WorldMap } from '../world/Map';
import { EntityManager } from '../entities/EntityManager';
import { BlueprintLoader } from './BlueprintLoader';

export enum GameState {
  LOADING = 'LOADING',
  ENTRY_SEQUENCE = 'ENTRY_SEQUENCE',
  MAIN_MENU = 'MAIN_MENU',
  GAMEPLAY = 'GAMEPLAY',
  KEEPER_INTERFACE = 'KEEPER_INTERFACE'
}

export class Game {
  private state: GameState = GameState.LOADING;
  private worldMap: WorldMap;
  private entityManager: EntityManager;
  private blueprintLoader: BlueprintLoader;
  private stateChangeListeners: ((newState: GameState) => void)[] = [];
  private keeperStatus: string = "Nominal"; // New property for Keeper UI interaction

  constructor(worldMap: WorldMap, entityManager: EntityManager, blueprintLoader: BlueprintLoader) {
    this.worldMap = worldMap;
    this.entityManager = entityManager;
    this.blueprintLoader = blueprintLoader;
  }

  public getState(): GameState {
    return this.state;
  }

  public setState(newState: GameState): void {
    if (this.state === newState) return;
    console.log(`State transition: ${this.state} -> ${newState}`);
    this.state = newState;
    this.stateChangeListeners.forEach(listener => listener(newState));
  }

  public getEntityManager(): EntityManager {
    return this.entityManager;
  }

  public startGame(): void {
    // Initial setup logic here
    this.setState(GameState.LOADING);
  }

  public addStateChangeListener(listener: (newState: GameState) => void): void {
    this.stateChangeListeners.push(listener);
  }

  public getKeeperStatus(): string {
    return this.keeperStatus;
  }

  public setKeeperStatus(status: string): void {
    this.keeperStatus = status;
  }
}