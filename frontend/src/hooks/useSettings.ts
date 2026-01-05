import { useState } from 'react';
import type { Settings } from '../types/settings';
import { DEFAULT_SETTINGS } from '../types/settings';

const STORAGE_KEY = 'mnb_settings';

export const useSettings = () => {
    const [settings, setSettings] = useState<Settings>(() => {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                return { ...DEFAULT_SETTINGS, ...JSON.parse(stored) };
            }
        } catch (error) {
            console.error('Failed to load settings:', error);
        }
        return DEFAULT_SETTINGS;
    });

    const updateSettings = (newSettings: Partial<Settings>) => {
        setSettings(prev => {
            const updated = { ...prev, ...newSettings };
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
            } catch (error) {
                console.error('Failed to save settings:', error);
            }
            return updated;
        });
    };

    const resetSettings = () => {
        setSettings(DEFAULT_SETTINGS);
        try {
            localStorage.removeItem(STORAGE_KEY);
        } catch (error) {
            console.error('Failed to reset settings:', error);
        }
    };

    return {
        settings,
        updateSettings,
        resetSettings,
    };
};
