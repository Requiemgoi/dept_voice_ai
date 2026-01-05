import React, { useState } from 'react';
import { ActionButtons } from './ActionButtons';
import type { Client } from '../../types/client';
import { STATUS_LABELS, CATEGORY_LABELS } from '../../utils/constants';
import { motion } from 'framer-motion';
import { ChevronLeft, ChevronRight, Search } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface ClientsTableProps {
    clients: Client[];
    total: number;
    page: number;
    onPageChange: (page: number) => void;
    onProcess: (id: number) => void;
    onViewDetails: (client: Client) => void;
    isLoading?: boolean;
}

const statusStyles = {
    pending: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
    processing: "bg-blue-500/10 text-blue-500 border-blue-500/20",
    completed: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
    failed: "bg-red-500/10 text-red-500 border-red-500/20",
};

export const ClientsTable: React.FC<ClientsTableProps> = ({
    clients,
    total,
    page,
    onPageChange,
    onProcess,
    onViewDetails,
    isLoading = false,
}) => {
    const [processingId, setProcessingId] = useState<number | null>(null);

    const handleProcess = async (id: number) => {
        setProcessingId(id);
        try {
            await onProcess(id);
        } finally {
            setProcessingId(null);
        }
    };

    const totalPages = Math.ceil(total / 25);

    return (
        <div className="space-y-4">
            <div className="glass rounded-xl border border-purple-500/20 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-purple-500/20 bg-purple-500/5">
                                <th className="p-4 font-medium text-muted-foreground">ID</th>
                                <th className="p-4 font-medium text-muted-foreground">ФИО</th>
                                <th className="p-4 font-medium text-muted-foreground">ИИН</th>
                                <th className="p-4 font-medium text-muted-foreground">Кредитор</th>
                                <th className="p-4 font-medium text-muted-foreground">Долг</th>
                                <th className="p-4 font-medium text-muted-foreground">Просрочка</th>
                                <th className="p-4 font-medium text-muted-foreground">Телефон</th>
                                <th className="p-4 font-medium text-muted-foreground">Статус</th>
                                <th className="p-4 font-medium text-muted-foreground">Категория</th>
                                <th className="p-4 font-medium text-muted-foreground">Действия</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-purple-500/10">
                            {isLoading ? (
                                Array.from({ length: 5 }).map((_, i) => (
                                    <tr key={i} className="animate-pulse">
                                        <td colSpan={10} className="p-4">
                                            <div className="h-8 bg-white/5 rounded"></div>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                clients.map((client, index) => (
                                    <motion.tr
                                        key={client.id}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.05 }}
                                        className="hover:bg-white/5 transition-colors group"
                                    >
                                        <td className="p-4 text-sm font-mono text-muted-foreground">{client.id}</td>
                                        <td className="p-4 font-medium text-white">{client.fio}</td>
                                        <td className="p-4 text-sm text-muted-foreground">{client.iin}</td>
                                        <td className="p-4 text-sm text-white">{client.creditor}</td>
                                        <td className="p-4 font-mono font-medium text-cyan-400">
                                            {client.amount.toLocaleString()} ₸
                                        </td>
                                        <td className="p-4">
                                            <span className={`text-sm ${client.days_overdue > 90 ? 'text-red-400' : 'text-emerald-400'}`}>
                                                {client.days_overdue} дн.
                                            </span>
                                        </td>
                                        <td className="p-4 text-sm text-muted-foreground">{client.phone}</td>
                                        <td className="p-4">
                                            <span className={`px-2 py-1 rounded-full text-xs border ${statusStyles[client.status] || 'bg-gray-500/10 text-gray-400 border-gray-500/20'}`}>
                                                {STATUS_LABELS[client.status]}
                                            </span>
                                        </td>
                                        <td className="p-4">
                                            {client.category ? (
                                                <span className="px-2 py-1 rounded-full text-xs bg-white/5 border border-white/10 text-gray-300">
                                                    {CATEGORY_LABELS[client.category]}
                                                </span>
                                            ) : (
                                                <span className="text-muted-foreground">—</span>
                                            )}
                                        </td>
                                        <td className="p-4">
                                            <ActionButtons
                                                client={client}
                                                onProcess={handleProcess}
                                                onViewDetails={onViewDetails}
                                                isProcessing={processingId === client.id}
                                            />
                                        </td>
                                    </motion.tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between px-4">
                <p className="text-sm text-muted-foreground">
                    Всего: {total} записей
                </p>
                <div className="flex items-center gap-2">
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onPageChange(page - 1)}
                        disabled={page <= 1 || isLoading}
                        className="hover:bg-white/10"
                    >
                        <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <span className="text-sm text-white font-medium">
                        Страница {page} из {totalPages || 1}
                    </span>
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onPageChange(page + 1)}
                        disabled={page >= totalPages || isLoading}
                        className="hover:bg-white/10"
                    >
                        <ChevronRight className="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>
    );
};
