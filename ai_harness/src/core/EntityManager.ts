export class EntityManager {
  private entities: Map<string, any> = new Map();
  addEntity(id: string, data: any) {
    this.entities.set(id, data);
  }
  getEntity(id: string) {
    return this.entities.get(id);
  }
  removeEntity(id: string) {
    this.entities.delete(id);
  }
}