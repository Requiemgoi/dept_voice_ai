import { useEffect } from 'react';
import { useSettings } from '../hooks/useSettings';
import { apiClient } from '../api/client';

/**
 * Hook to apply settings to the application
 * - Updates API base URL when it changes
 * - Can be extended to apply theme, language, etc.
 */
export const useApplySettings = () => {
    const { settings } = useSettings();

    useEffect(() => {
        // Update API base URL when settings change
        apiClient.defaults.baseURL = settings.apiUrl;
    }, [settings.apiUrl]);

    // Theme switching disabled - always use light theme
    // useEffect(() => {
    //     const root = document.documentElement;
    //     console.log('Applying theme:', settings.theme);
    //     if (settings.theme === 'dark') {
    //         root.classList.add('dark');
    //         console.log('Dark mode enabled');
    //     } else {
    //         root.classList.remove('dark');
    //         console.log('Light mode enabled');
    //     }
    // }, [settings.theme]);

    // TODO: Apply language settings
    // TODO: Apply auto-refresh interval
};
