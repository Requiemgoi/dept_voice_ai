export type Language = 'ru' | 'en' | 'kk';
export type Theme = 'light' | 'dark';

export interface Settings {
    apiUrl: string;
    language: Language;
    theme: Theme;
    demoMode: boolean;
    autoRefreshInterval: number; // in seconds, 0 = disabled
}

export const DEFAULT_SETTINGS: Settings = {
    apiUrl: 'http://localhost:8000',
    language: 'ru',
    theme: 'light', // Always light theme
    demoMode: true,
    autoRefreshInterval: 0,
};
