import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Download, Plus } from 'lucide-react';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale/ru';

import { MainLayout } from '../components/layout/MainLayout';
import { UploadZone } from '../components/upload/UploadZone';
import { ClientsTable } from '../components/table/ClientsTable';
import { Modal } from '../components/ui/Modal';
import { Button } from '../components/ui/Button';

import { useClients } from '../hooks/useClients';
import { useUpload } from '../hooks/useUpload';
import { useSettings } from '../hooks/useSettings';
import { processClient, exportResults } from '../api/endpoints/clients';

import type { Client } from '../types/client';
import { CATEGORY_LABELS, STATUS_LABELS } from '../utils/constants';

export const ClientsPage: React.FC = () => {
    const [page, setPage] = useState(1);
    const [selectedClient, setSelectedClient] = useState<Client | null>(null);
    const [showUpload, setShowUpload] = useState(false);

    const { settings } = useSettings();
    const queryClient = useQueryClient();
    const { data, isLoading } = useClients({ page, limit: 25 });
    const uploadMutation = useUpload();

    const processMutation = useMutation({
        mutationFn: (id: number) => processClient(id, settings.demoMode),
        onSuccess: (data: any) => {
            toast.success('Клиент успешно обработан');

            // Play TTS audio if available
            if (data?.tts_audio_url) {
                const audio = new Audio(data.tts_audio_url);
                const playPromise = audio.play();

                if (playPromise !== undefined) {
                    playPromise.catch(error => {
                        console.error("Audio playback failed:", error);
                        toast.error("Не удалось воспроизвести аудио");
                    });
                }
            }

            queryClient.invalidateQueries({ queryKey: ['clients'] });
        },
        onError: (error: any) => {
            const message = error.response?.data?.detail || 'Ошибка обработки';
            toast.error(message);
        },
    });

    const exportMutation = useMutation({
        mutationFn: exportResults,
        onSuccess: (blob) => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `clients_export_${format(new Date(), 'yyyy-MM-dd_HH-mm')}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            toast.success('Результаты экспортированы');
        },
        onError: () => {
            toast.error('Ошибка экспорта');
        },
    });

    const handleUpload = (file: File) => {
        uploadMutation.mutate(file, {
            onSuccess: () => {
                setShowUpload(false);
            }
        });
    };

    const handleProcess = (id: number) => {
        processMutation.mutate(id);
    };

    const handleViewDetails = (client: Client) => {
        setSelectedClient(client);
    };

    const handleExport = () => {
        exportMutation.mutate();
    };

    return (
        <MainLayout>
            <div className="p-8">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">Клиенты</h1>
                            <p className="text-gray-400 mt-1">
                                База должников для обзвона
                            </p>
                        </div>

                        <div className="flex items-center gap-3">
                            <Button
                                variant="secondary"
                                onClick={handleExport}
                                isLoading={exportMutation.isPending}
                                disabled={!data?.items?.length}
                            >
                                <Download className="w-4 h-4 mr-2" />
                                Экспорт
                            </Button>

                            <Button
                                variant="primary"
                                onClick={() => setShowUpload(true)}
                            >
                                <Plus className="w-4 h-4 mr-2" />
                                Загрузить Excel
                            </Button>
                        </div>
                    </div>
                </div>

                {/* Content */}
                {data?.items?.length === 0 && !isLoading ? (
                    <div className="glass rounded-lg border border-purple-500/20 p-12 text-center">
                        <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-4">
                            <Plus className="w-8 h-8 text-purple-400" />
                        </div>
                        <h3 className="text-lg font-medium text-white mb-2">Нет клиентов</h3>
                        <p className="text-gray-400 mb-6">Загрузите базу клиентов из Excel файла для начала работы</p>
                        <Button
                            variant="primary"
                            onClick={() => setShowUpload(true)}
                        >
                            Загрузить базу
                        </Button>
                    </div>
                ) : (
                    <ClientsTable
                        clients={data?.items || []}
                        total={data?.total || 0}
                        page={page}
                        onPageChange={setPage}
                        onProcess={handleProcess}
                        onViewDetails={handleViewDetails}
                        isLoading={isLoading}
                    />
                )}

                {/* Upload Modal */}
                <Modal
                    isOpen={showUpload}
                    onClose={() => setShowUpload(false)}
                    title="Загрузка клиентов"
                >
                    <UploadZone
                        onUpload={handleUpload}
                        isUploading={uploadMutation.isPending}
                    />
                </Modal>

                {/* Client Details Modal */}
                {selectedClient && (
                    <Modal
                        isOpen={!!selectedClient}
                        onClose={() => setSelectedClient(null)}
                        title="Детали клиента"
                        footer={
                            <div className="flex justify-end gap-3">
                                <Button variant="secondary" onClick={() => setSelectedClient(null)}>
                                    Закрыть
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        handleProcess(selectedClient.id);
                                        setSelectedClient(null);
                                    }}
                                    disabled={selectedClient.status !== 'pending' && selectedClient.status !== 'failed'}
                                >
                                    Обработать
                                </Button>
                            </div>
                        }
                    >
                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="text-sm text-gray-500">ID</p>
                                    <p className="font-semibold">{selectedClient.id}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500">Статус</p>
                                    <p className="font-semibold">{STATUS_LABELS[selectedClient.status]}</p>
                                </div>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500">ФИО</p>
                                <p className="font-semibold">{selectedClient.fio}</p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500">ИИН</p>
                                <p className="font-semibold">{selectedClient.iin}</p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500">Кредитор</p>
                                <p className="font-semibold">{selectedClient.creditor}</p>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="text-sm text-gray-500">Сумма долга</p>
                                    <p className="font-semibold text-lg">{selectedClient.amount.toLocaleString()} ₸</p>
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500">Дни просрочки</p>
                                    <p className="font-semibold text-lg">{selectedClient.days_overdue} дн.</p>
                                </div>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500">Телефон</p>
                                <p className="font-semibold">{selectedClient.phone}</p>
                            </div>

                            {selectedClient.category && (
                                <div>
                                    <p className="text-sm text-gray-500">Категория</p>
                                    <p className="font-semibold">{CATEGORY_LABELS[selectedClient.category]}</p>
                                </div>
                            )}

                            <div>
                                <p className="text-sm text-gray-500">Дата создания</p>
                                <p className="font-semibold">
                                    {format(new Date(selectedClient.created_at), 'dd MMMM yyyy, HH:mm', { locale: ru })}
                                </p>
                            </div>

                            {selectedClient.processed_at && (
                                <div>
                                    <p className="text-sm text-gray-500">Дата обработки</p>
                                    <p className="font-semibold">
                                        {format(new Date(selectedClient.processed_at), 'dd MMMM yyyy, HH:mm', { locale: ru })}
                                    </p>
                                </div>
                            )}
                        </div>
                    </Modal>
                )}
            </div>
        </MainLayout>
    );
};
