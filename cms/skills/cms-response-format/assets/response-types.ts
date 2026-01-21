/**
 * CMS Response Type Definitions
 * Standardized Strapi-style response format
 */

// Base response structure
export interface Response<T> {
  data: T | T[] | null;
  error: Error | null;
  meta?: Meta;
}

// List response with pagination
export interface ListResponse<T> {
  data: T[];
  meta: Meta;
}

// Error response
export interface ErrorResponse {
  error: Error;
  data: null;
  meta?: Meta;
}

// Error object
export interface Error {
  code?: number;
  status?: number;
  name?: string;
  message: string;
  details?: any;
}

// Meta information
export interface Meta {
  pagination?: Pagination;
  traceId?: string;
  took?: number;
}

// Pagination information
export interface Pagination {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
  hasMore: boolean;
}

// Generic entity with timestamps
export interface Entity {
  id: string | number;
  createdAt: string;
  updatedAt: string;
}

// API Client interface
export interface ApiClient {
  get<T>(path: string, params?: Record<string, any>): Promise<T>;
  post<T>(path: string, body?: any): Promise<T>;
  put<T>(path: string, body?: any): Promise<T>;
  delete<T>(path: string): Promise<T>;
}

// API Error class
export class ApiError extends Error {
  constructor(
    message: string,
    public code?: number,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Hook response types
export interface UseApiResponse<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}
