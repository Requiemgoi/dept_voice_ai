import { apiClient } from '../client';
import type {
    Client,
    ClientsResponse,
    UploadResponse,
    ProcessResponse
} from '../../types/client';
import type { QueryParams } from '../../types/api';

export const uploadExcel = async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<UploadResponse>('/api/v1/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

export const getClients = async (params?: QueryParams): Promise<ClientsResponse> => {
    const response = await apiClient.get<ClientsResponse>('/api/v1/clients', {
        params: {
            page: params?.page || 1,
            limit: params?.limit || 25,
            ...params,
        },
    });

    return response.data;
};

export const getClient = async (id: number): Promise<Client> => {
    const response = await apiClient.get<Client>(`/api/v1/clients/${id}`);
    return response.data;
};

export const processClient = async (
    id: number,
    useDemo: boolean = false
): Promise<ProcessResponse> => {
    const response = await apiClient.post<ProcessResponse>(
        `/api/v1/process/${id}`,
        { use_demo: useDemo }
    );

    return response.data;
};

export const uploadResponse = async (
    id: number,
    audioBlob: Blob
): Promise<ProcessResponse> => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'response.wav');

    const response = await apiClient.post<ProcessResponse>(
        `/api/v1/process/${id}/response`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );

    return response.data;
};

export const exportResults = async (status?: string, category?: string): Promise<Blob> => {
    const response = await apiClient.get('/api/v1/export', {
        params: { status, category },
        responseType: 'blob',
    });

    return response.data;
};
