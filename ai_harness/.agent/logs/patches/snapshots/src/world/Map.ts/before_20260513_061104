/**
 * @fileoverview Core implementation for the sparse, expanding world map.
 * Uses a JavaScript Map to store cell data keyed by coordinate strings "x,y".
 */

// --- Types and Interfaces ---

type TerrainType = 'Vines' | 'Biomass' | 'Clear' | 'HabitableZone';

interface MapCell {
  terrain: TerrainType;
  entities: Set<string>;
  // Add other necessary cell properties here
}

export class WorldMap {
  private cells: Map<string, MapCell> = new Map();

  /**
   * Gets the key for a given coordinate.
   * @param x The x-coordinate.
   * @param y The y-coordinate.
   * @returns The coordinate key string.
   */
  private getCellKey(x: number, y: number): string {
    return `${x},${y}`;
  }

  /**
   * Sets the terrain for a given coordinate.
   * @param x The x-coordinate.
   * @param y The y-coordinate.
   * @param terrain The terrain type.
   */
  public setTerrain(x: number, y: number, terrain: TerrainType): void {
    const key = this.getCellKey(x, y);
    if (!this.cells.has(key)) {
      this.cells.set(key, { terrain: terrain, entities: new Set() });
    } else {
      const cell = this.cells.get(key)!;
      cell.terrain = terrain;
    }
  }

  /**
   * Gets the terrain for a given coordinate.
   * @param x The x-coordinate.
   * @param y The y-coordinate.
   * @returns The terrain type or undefined if not set.
   */
  public getTerrain(x: number, y: number): TerrainType | undefined {
    return this.cells.get(this.getCellKey(x, y))?.terrain;
  }
}