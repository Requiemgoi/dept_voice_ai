import React from 'react';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { Chip } from '@mui/material';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale/ru';
import type { CallRecordWithClient, Category } from '../../types/client';
import { CATEGORY_LABELS, CATEGORY_COLORS } from '../../utils/constants';

interface HistoryTableProps {
    records: CallRecordWithClient[];
    total: number;
    page: number;
    onPageChange: (page: number) => void;
    isLoading?: boolean;
}

export const HistoryTable: React.FC<HistoryTableProps> = ({
    records,
    total,
    page,
    onPageChange,
    isLoading = false,
}) => {
    const columns: GridColDef[] = [
        {
            field: 'created_at',
            headerName: 'Дата и время',
            width: 180,
            renderCell: (params: GridRenderCellParams) => (
                <span className="text-gray-600">
                    {format(new Date(params.value), 'dd.MM.yyyy HH:mm', { locale: ru })}
                </span>
            ),
        },
        {
            field: 'client',
            headerName: 'Клиент',
            width: 200,
            valueGetter: (params) => params.row.client?.fio,
        },
        {
            field: 'transcript',
            headerName: 'Транскрипт',
            width: 300,
            sortable: false,
            renderCell: (params: GridRenderCellParams) => (
                <span className="text-gray-700 truncate block w-full" title={params.value}>
                    {params.value || '—'}
                </span>
            ),
        },
        {
            field: 'category',
            headerName: 'Категория',
            width: 150,
            renderCell: (params: GridRenderCellParams) => {
                if (!params.value) return <span className="text-gray-400">—</span>;

                return (
                    <Chip
                        label={CATEGORY_LABELS[params.value as Category] || params.value}
                        size="small"
                        sx={{
                            backgroundColor: CATEGORY_COLORS[params.value as Category] || '#6B7280',
                            color: 'white',
                            fontWeight: 500,
                        }}
                    />
                );
            },
        },
        {
            field: 'confidence',
            headerName: 'Уверенность',
            width: 120,
            renderCell: (params: GridRenderCellParams) => (
                <span className={`font-medium ${(params.value as number) > 0.8 ? 'text-green-600' : 'text-orange-600'}`}>
                    {Math.round((params.value as number) * 100)}%
                </span>
            ),
        },
        {
            field: 'detected_language',
            headerName: 'Язык',
            width: 80,
            renderCell: (params: GridRenderCellParams) => (
                <span className="uppercase text-xs font-bold text-gray-400">
                    {(params.value as string) || '—'}
                </span>
            ),
        },
    ];

    return (
        <div className="w-full h-[600px] bg-white rounded-lg shadow-sm border border-gray-200">
            <DataGrid
                rows={records}
                columns={columns}
                paginationMode="server"
                rowCount={total}
                paginationModel={{
                    page: page - 1,
                    pageSize: 20,
                }}
                onPaginationModelChange={(model) => onPageChange(model.page + 1)}
                loading={isLoading}
                disableRowSelectionOnClick
                sx={{
                    border: 'none',
                    '& .MuiDataGrid-cell': {
                        borderBottom: '1px solid #f3f4f6',
                    },
                    '& .MuiDataGrid-columnHeaders': {
                        backgroundColor: '#f9fafb',
                        borderBottom: '2px solid #e5e7eb',
                        fontWeight: 600,
                    },
                }}
            />
        </div>
    );
};
