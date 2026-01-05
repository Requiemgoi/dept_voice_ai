import { useQuery } from '@tanstack/react-query';
import { getStatistics } from '../api/endpoints/analytics';

export const useAnalytics = () => {
    return useQuery({
        queryKey: ['analytics'],
        queryFn: getStatistics,
        refetchInterval: 30000, // Refresh every 30 seconds
    });
};
