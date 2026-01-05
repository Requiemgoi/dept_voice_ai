export interface ApiError {
    message: string;
    detail?: string;
}

export interface PaginationParams {
    page?: number;
    limit?: number;
}

export interface QueryParams extends PaginationParams {
    status?: string;
    category?: string;
}
