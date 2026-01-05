import { apiClient } from '../client';

export interface AnalyticsData {
    summary: {
        total_clients: number;
        completed: number;
        processing: number;
        failed: number;
        pending: number;
        success_rate: number;
    };
    categories: Record<string, number>;
    daily_activity: Array<{ date: string; count: number }>;
}

export const getStatistics = async (): Promise<AnalyticsData> => {
    const response = await apiClient.get<AnalyticsData>('/api/v1/statistics');
    return response.data;
};
