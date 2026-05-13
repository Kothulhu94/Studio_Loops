/**
 * @fileoverview Manages all active entities within the game world.
 */

import { WorldMap } from '../world/Map';

interface Entity {
    id: string;
    position: { x: number, y: number };
    type: string;
    health: number;
    // Other entity properties
}

export class EntityManager {
    private entities: Map<string, Entity> = new Map();
    private nextEntityId: number = 1;

    constructor(private map: WorldMap) {}

    /**
     * Creates and adds a new entity to the manager.
     * @param type The type of entity to create.
     * @param position Initial position.
     * @returns The newly created entity.
     */
    public createEntity(type: string, position: { x: number, y: number }): Entity {
        const id = `e_${this.nextEntityId++}`;
        const newEntity: Entity = {
            id: id,
            position: position,
            type: type,
            health: 100
        };
        this.entities.set(id, newEntity);
        // Optionally, register entity position with the map if needed
        return newEntity;
    }

    /**
     * Retrieves an entity by its ID.
     * @param id The entity ID.
     * @returns The entity or undefined.
     */
    public getEntity(id: string): Entity | undefined {
        return this.entities.get(id);
    }

    /**
     * Updates the position of an existing entity.
     * @param id The entity ID.
     * @param newPosition The new position.
     * @returns True if the entity was found and updated, false otherwise.
     */
    public updateEntityPosition(id: string, newPosition: { x: number, y: number }): boolean {
        const entity = this.entities.get(id);
        if (entity) {
            entity.position = newPosition;
            return true;
        }
        return false;
    }

    /**
     * Removes an entity from the manager.
     * @param id The entity ID.
     * @returns True if the entity was found and removed, false otherwise.
     */
    public destroyEntity(id: string): boolean {
        return this.entities.delete(id);
    }

    public getAllEntities(): Entity[] {
        return Array.from(this.entities.values());
    }
}
