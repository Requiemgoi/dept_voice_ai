export interface Client {
    id: number;
    fio: string;
    iin: string;
    creditor: string;
    amount: number;
    days_overdue: number;
    phone: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    category?: Category;
    created_at: string;
    processed_at?: string;
}

export type Category =
    | 'ignore'
    | 'promise'
    | 'help'
    | 'wrong_number'
    | 'third_party'
    | 'hangup'
    | 'unknown';

export interface CallRecord {
    id: number;
    client_id: number;
    tts_text: string;
    transcript: string;
    detected_language: 'ru' | 'kk';
    category: Category;
    confidence: number;
    metadata: {
        promised_date?: string;
        reason?: string;
        matched_keywords?: string[];
    };
    created_at: string;
}

export interface ClientsResponse {
    items: Client[];
    total: number;
    page: number;
    limit: number;
}

export interface CallRecordWithClient extends CallRecord {
    client: Client;
}

export interface CallHistoryResponse {
    items: CallRecordWithClient[];
    total: number;
    page: number;
    limit: number;
}

export interface UploadResponse {
    message: string;
    file_path: string;
    added_count: number;
    error_count: number;
}

export interface ProcessResponse {
    success: boolean;
    message: string;
    call_record?: CallRecord;
}
