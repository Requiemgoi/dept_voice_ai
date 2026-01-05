import axios from 'axios';

// Get API URL from settings or use default
const getApiUrl = () => {
    try {
        const stored = localStorage.getItem('mnb_settings');
        if (stored) {
            const settings = JSON.parse(stored);
            return settings.apiUrl || 'http://localhost:8000';
        }
    } catch (error) {
        console.error('Failed to load settings:', error);
    }
    return import.meta.env.VITE_API_URL || 'http://localhost:8000';
};

export const apiClient = axios.create({
    baseURL: getApiUrl(),
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000,
});

// Request interceptor
apiClient.interceptors.request.use(
    (config) => {
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
apiClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response) {
            // Server responded with error
            console.error('API Error:', error.response.data);
        } else if (error.request) {
            // Request made but no response
            console.error('Network Error:', error.message);
        } else {
            console.error('Error:', error.message);
        }
        return Promise.reject(error);
    }
);
