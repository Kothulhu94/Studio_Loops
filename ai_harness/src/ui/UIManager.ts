import { GameState } from '../engine/Game';

export class UIManager {
  private loadingScreen: HTMLElement | null;
  private entrySequence: HTMLElement | null;
  private mainMenu: HTMLElement | null;
  private progressText: HTMLElement | null;

  constructor() {
    this.loadingScreen = document.getElementById('loading-screen');
    this.entrySequence = document.getElementById('entry-sequence');
    this.mainMenu = document.getElementById('main-menu');
    this.progressText = document.getElementById('loading-progress');
  }

  public update(state: GameState): void {
    // Hide all screens
    this.toggleVisibility(this.loadingScreen, state === GameState.LOADING);
    this.toggleVisibility(this.entrySequence, state === GameState.ENTRY_SEQUENCE);
    this.toggleVisibility(this.mainMenu, state === GameState.MAIN_MENU);
  }

  public setLoadingProgress(percent: number): void {
    if (this.progressText) {
      this.progressText.innerHTML = `Decrypting Biospheric Data [${percent}%] <span class="cursor">_</span>`;
    }
  }

  private toggleVisibility(element: HTMLElement | null, visible: boolean): void {
    if (!element) return;
    if (visible) {
      element.classList.add('active');
    } else {
      element.classList.remove('active');
    }
  }
}