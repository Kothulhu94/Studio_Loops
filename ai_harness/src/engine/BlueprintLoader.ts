import { Blueprint } from './BlueprintSchema';

/**
 * Service for loading and validating Blueprints from JSON files.
 */
export class BlueprintLoader {
    /**
     * Loads a blueprint by its ID.
     * @param sceneId The ID of the scene to load.
     * @returns A promise that resolves to the Blueprint.
     */
    public async load(sceneId: string): Promise<Blueprint> {
        console.log(`Loading blueprint for scene: ${sceneId}`);
        
        // In a real implementation, this would fetch a JSON file.
        // For now, we simulate an async load.
        const response = await fetch(`/data/blueprints/${sceneId}.json`);
        if (!response.ok) {
            throw new Error(`Failed to load blueprint: ${sceneId}`);
        }
        
        const data = await response.json();
        return this.validate(data);
    }

    /**
     * Validates that the loaded data matches the Blueprint interface.
     */
    private validate(data: any): Blueprint {
        if (!data.sceneId || !data.requiredAssets || !data.uiOverlayConfig) {
            throw new Error('Invalid blueprint format: Missing required fields.');
        }
        return data as Blueprint;
    }
}
