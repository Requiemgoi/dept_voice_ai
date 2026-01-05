import type { Category } from '../types/client';

export const STATUS_LABELS: Record<string, string> = {
    pending: 'Ожидает',
    processing: 'Обрабатывается',
    completed: 'Завершено',
    failed: 'Ошибка',
};

export const STATUS_COLORS: Record<string, string> = {
    pending: '#F59E0B',
    processing: '#06B6D4',
    completed: '#10B981',
    failed: '#EF4444',
};

export const CATEGORY_LABELS: Record<Category, string> = {
    ignore: 'Игнорирует',
    promise: 'Обещал оплатить',
    help: 'Требуется помощь',
    wrong_number: 'Неверный номер',
    third_party: 'Третье лицо',
    hangup: 'Сброс',
    unknown: 'Неизвестно',
};

export const CATEGORY_COLORS: Record<Category, string> = {
    ignore: '#9CA3AF',
    promise: '#10B981',
    help: '#F59E0B',
    wrong_number: '#EF4444',
    third_party: '#6366F1',
    hangup: '#EF4444',
    unknown: '#6B7280',
};

export const ACCEPTED_FILE_TYPES = {
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'application/vnd.ms-excel': ['.xls'],
};

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
