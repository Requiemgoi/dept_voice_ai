import React, { useState } from 'react';
import { MainLayout } from '../components/layout/MainLayout';
import { HistoryTable } from '../components/table/HistoryTable';
import { useHistory } from '../hooks/useHistory';
import { Card } from '../components/ui/Card';
import { Phone, CheckCircle2, XCircle, Clock } from 'lucide-react';
import type { CallRecordWithClient } from '../types/client';

export const CallHistoryPage: React.FC = () => {
    const [page, setPage] = useState(1);
    const { data, isLoading } = useHistory({ page, limit: 20 });

    const processedCount = data?.items?.filter((i: CallRecordWithClient) => i.category && i.category !== 'unknown').length || 0;
    const pendingCount = data?.items?.filter((i: CallRecordWithClient) => !i.transcript).length || 0;

    return (
        <MainLayout>
            <div className="p-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">История звонков</h1>
                    <p className="text-gray-500 mt-1">Результаты всех совершенных обзвонов</p>
                </div>

                {/* Stats Summary */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-primary-100 rounded-lg">
                                <Phone className="w-6 h-6 text-primary-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Всего звонков</p>
                                <p className="text-2xl font-bold">{data?.total || 0}</p>
                            </div>
                        </div>
                    </Card>
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-green-100 rounded-lg">
                                <CheckCircle2 className="w-6 h-6 text-green-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Успешно</p>
                                <p className="text-2xl font-bold">
                                    {processedCount}
                                </p>
                            </div>
                        </div>
                    </Card>
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-orange-100 rounded-lg">
                                <Clock className="w-6 h-6 text-orange-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Ожидают</p>
                                <p className="text-2xl font-bold">
                                    {pendingCount}
                                </p>
                            </div>
                        </div>
                    </Card>
                    <Card>
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-red-100 rounded-lg">
                                <XCircle className="w-6 h-6 text-red-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Ошибки</p>
                                <p className="text-2xl font-bold">0</p>
                            </div>
                        </div>
                    </Card>
                </div>

                <HistoryTable
                    records={data?.items || []}
                    total={data?.total || 0}
                    page={page}
                    onPageChange={setPage}
                    isLoading={isLoading}
                />
            </div>
        </MainLayout>
    );
};
