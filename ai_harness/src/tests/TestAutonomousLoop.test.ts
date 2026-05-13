import { describe, it, expect, vi } from 'vitest';
import { EntityManager } from '../core/EntityManager';

describe('AutonomousLoop', () => {
  it('should manage entities', () => {
    const em = new EntityManager();
    em.addEntity('1', { type: 'player' });
    expect(em.getEntity('1').type).toBe('player');
  });
});