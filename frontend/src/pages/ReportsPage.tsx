import React, { useState } from 'react';
import { MainLayout } from '../components/layout/MainLayout';
import { useMutation } from '@tanstack/react-query';
import { exportResults } from '../api/endpoints/clients';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { MenuItem, Select, FormControl, InputLabel, CircularProgress } from '@mui/material';
import { Download, FileSpreadsheet, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import { STATUS_LABELS, CATEGORY_LABELS } from '../utils/constants';

export const ReportsPage: React.FC = () => {
    const [status, setStatus] = useState<string>('');
    const [category, setCategory] = useState<string>('');

    const exportMutation = useMutation({
        mutationFn: () => exportResults(status || undefined, category || undefined),
        onSuccess: (blob) => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const statusSuffix = status ? `_${status}` : '';
            const categorySuffix = category ? `_${category}` : '';
            a.download = `report${statusSuffix}${categorySuffix}_${format(new Date(), 'yyyyMMdd_HHmm')}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            toast.success('Отчет успешно сформирован и скачан');
        },
        onError: (error: any) => {
            toast.error(error.response?.data?.detail || 'Ошибка при генерации отчета');
        },
    });

    const handleExport = () => {
        exportMutation.mutate();
    };

    return (
        <MainLayout>
            <div className="p-8 max-w-4xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Отчеты</h1>
                    <p className="text-gray-500 mt-1">Экспорт данных и формирование отчетов</p>
                </div>

                <div className="grid grid-cols-1 gap-8">
                    <Card title="Настроить выгрузку">
                        <div className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <FormControl fullWidth size="small">
                                    <InputLabel>Статус клиента</InputLabel>
                                    <Select
                                        value={status}
                                        label="Статус клиента"
                                        onChange={(e) => setStatus(e.target.value)}
                                    >
                                        <MenuItem value="">Все статусы</MenuItem>
                                        {Object.entries(STATUS_LABELS).map(([key, label]) => (
                                            <MenuItem key={key} value={key}>{label}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>

                                <FormControl fullWidth size="small">
                                    <InputLabel>Результат (Категория)</InputLabel>
                                    <Select
                                        value={category}
                                        label="Результат (Категория)"
                                        onChange={(e) => setCategory(e.target.value)}
                                    >
                                        <MenuItem value="">Все категории</MenuItem>
                                        {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
                                            <MenuItem key={key} value={key}>{label}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                            </div>

                            <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 flex gap-4">
                                <div className="p-2 bg-blue-100 rounded-full h-fit">
                                    <AlertCircle className="w-5 h-5 text-blue-600" />
                                </div>
                                <div className="text-sm text-blue-800">
                                    <p className="font-semibold mb-1">Информация об экспорте</p>
                                    <p>Вы получите Excel файл со всеми данными клиентов, включая ИИН, суммы и результаты последних звонков. Файл будет подготовлен моментально на основе текущих данных в системе.</p>
                                </div>
                            </div>

                            <div className="flex justify-end">
                                <Button
                                    variant="primary"
                                    onClick={handleExport}
                                    disabled={exportMutation.isPending}
                                    className="w-full md:w-auto"
                                >
                                    {exportMutation.isPending ? (
                                        <CircularProgress size={20} color="inherit" className="mr-2" />
                                    ) : (
                                        <FileSpreadsheet className="w-4 h-4 mr-2" />
                                    )}
                                    Сформировать Excel
                                </Button>
                            </div>
                        </div>
                    </Card>

                    {/* Predefined Reports */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <Card onClick={() => { setStatus('completed'); handleExport(); }} className="hover:border-green-500/50">
                            <div className="flex flex-col items-center text-center">
                                <div className="p-3 bg-green-100 rounded-full mb-3">
                                    <CheckCircle className="w-6 h-6 text-green-600" />
                                </div>
                                <h4 className="font-semibold">Только успешные</h4>
                                <p className="text-xs text-gray-500 mt-1">Клиенты, которые завершили звонок</p>
                            </div>
                        </Card>

                        <Card onClick={() => { setStatus('pending'); handleExport(); }} className="hover:border-orange-500/50">
                            <div className="flex flex-col items-center text-center">
                                <div className="p-3 bg-orange-100 rounded-full mb-3">
                                    <Clock className="w-6 h-6 text-orange-600" />
                                </div>
                                <h4 className="font-semibold">Ожидающие</h4>
                                <p className="text-xs text-gray-500 mt-1">Клиенты в очереди на обзвон</p>
                            </div>
                        </Card>

                        <Card onClick={() => { handleExport(); }} className="hover:border-blue-500/50">
                            <div className="flex flex-col items-center text-center">
                                <div className="p-3 bg-blue-100 rounded-full mb-3">
                                    <Download className="w-6 h-6 text-blue-600" />
                                </div>
                                <h4 className="font-semibold">Полная база</h4>
                                <p className="text-xs text-gray-500 mt-1">Экспорт всех данных системы</p>
                            </div>
                        </Card>
                    </div>
                </div>
            </div>
        </MainLayout>
    );
};
