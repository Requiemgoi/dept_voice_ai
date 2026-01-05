import { apiClient } from '../client';
import type { CallHistoryResponse } from '../../types/client';
import type { QueryParams } from '../../types/api';

export const getCallHistory = async (params?: QueryParams): Promise<CallHistoryResponse> => {
    const response = await apiClient.get<CallHistoryResponse>('/api/v1/history', {
        params: {
            page: params?.page || 1,
            limit: params?.limit || 20,
            ...params,
        },
    });

    return response.data;
};
