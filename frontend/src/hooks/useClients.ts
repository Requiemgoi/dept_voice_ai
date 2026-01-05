import { useQuery } from '@tanstack/react-query';
import { getClients, getClient } from '../api/endpoints/clients';
import type { QueryParams } from '../types/api';

export const useClients = (params?: QueryParams) => {
    return useQuery({
        queryKey: ['clients', params],
        queryFn: () => getClients(params),
        refetchInterval: 10000, // Refetch every 10 seconds
        staleTime: 5000,
    });
};

export const useClient = (id: number) => {
    return useQuery({
        queryKey: ['client', id],
        queryFn: () => getClient(id),
        enabled: !!id,
    });
};
