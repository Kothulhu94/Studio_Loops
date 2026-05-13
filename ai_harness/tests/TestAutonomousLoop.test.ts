import { describe, it, expect } from 'vitest';
import { EntityManager } from '../src/entities/EntityManager';
import { WorldMap } from '../src/world/Map';

describe('EntityManager', () => {
  it('should create and manage entities', () => {
    const map = new WorldMap();
    const em = new EntityManager(map);
    const entity = em.createEntity('player', { x: 0, y: 0 });
    
    expect(entity.type).toBe('player');
    expect(em.getEntity(entity.id)).toBeDefined();
  });
});