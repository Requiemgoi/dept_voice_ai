import { useMutation, useQueryClient } from '@tanstack/react-query';
import { uploadExcel } from '../api/endpoints/clients';
import toast from 'react-hot-toast';

export const useUpload = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: uploadExcel,
        onSuccess: (data) => {
            if (data.added_count > 0) {
                toast.success(`Успешно загружено ${data.added_count} клиентов`);
            }

            if (data.error_count > 0) {
                toast.error(`Пропущено ${data.error_count} записей (дубликаты или ошибки)`);
            }

            if (data.added_count === 0 && data.error_count === 0) {
                toast('Файл пуст или не содержит новых данных', { icon: '⚠️' });
            }

            queryClient.invalidateQueries({ queryKey: ['clients'] });
        },
        onError: (error: any) => {
            const message = error.response?.data?.detail || error.message || 'Ошибка загрузки файла';
            toast.error(message);
        },
    });
};
