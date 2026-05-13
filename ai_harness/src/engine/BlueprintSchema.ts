/**
 * Defines the structure for Scene configurations, UI layouts, and asset dependencies.
 */
export interface Blueprint {
    sceneId: string;
    requiredAssets: AssetManifest[];
    initialState: Record<string, any>;
    uiOverlayConfig: UIConfig;
}

export interface AssetManifest {
    id: string;
    type: 'sprite' | 'sound' | 'json' | 'tileset';
    path: string;
}

export interface UIConfig {
    layout: 'menu' | 'hud' | 'dialogue';
    components: UIComponentConfig[];
}

export interface UIComponentConfig {
    id: string;
    type: string;
    position: { x: number; y: number };
    props: Record<string, any>;
}
