import { useQuery } from '@tanstack/react-query';
import { getCallHistory } from '../api/endpoints/history';
import type { QueryParams } from '../types/api';

export const useHistory = (params?: QueryParams) => {
    return useQuery({
        queryKey: ['history', params],
        queryFn: () => getCallHistory(params),
    });
};
