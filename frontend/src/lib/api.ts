/**
 * API Client Module
 * 
 * Design Pattern: Singleton API Client
 * - Centralized HTTP client configuration
 * - Consistent error handling across all requests
 * - Environment-aware base URL (dev vs production)
 * 
 * Benefits:
 * - Single point of configuration
 * - Easy to add interceptors (auth, logging)
 * - Type-safe API methods
 */

import axios from 'axios';

// Environment Configuration: Supports both local dev and production
// Vite automatically injects environment variables at build time
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// Axios Instance: Pre-configured client for all API requests
// Using instance pattern allows shared configuration and interceptors
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface VaccineRecord {
  region: string;
  brand: string;
  year: number;
  market_size_usd: number;
  avg_price_usd: number;
  doses_sold_million: number;
  growth_rate_percent: number;
  insight: string;
}

export interface VaccineListResponse {
  total: number;
  returned: number;
  data: VaccineRecord[];
}

export interface SummaryKPI {
  label: string;
  value: number;
  unit: string | null;
  description: string | null;
}

export interface SummaryResponse {
  kpis: SummaryKPI[];
  filters_applied: {
    region: string | null;
    brand: string | null;
    year: number | null;
  };
}

export interface VaccineFilters {
  region?: string;
  brand?: string;
  year?: number;
  limit?: number;
  offset?: number;
}

export interface ChatRequest {
  query: string;
  region?: string;
  brand?: string;
  year?: number;
}

export interface ChatResponse {
  answer: string;
  visualization: string | null;
  confidence: number;
}

export interface PredictionResponse {
  predictions: Array<{
    year: number;
    predicted_market_size_usd: number;
    predicted_avg_price_usd: number;
    predicted_growth_rate_percent: number;
    confidence_interval_lower: number;
    confidence_interval_upper: number;
  }>;
  confidence: number;
  method: string;
  ai_insight: string | null;
}

export interface Recommendation {
  title: string;
  description: string;
  action: {
    type: string;
    field?: string;
  };
}

/**
 * API Service Object
 * 
 * Encapsulates all API calls in a single object for:
 * - Better organization and discoverability
 * - Consistent error handling
 * - Type safety with TypeScript generics
 */
export const vaccineApi = {
  /**
   * Fetch vaccine market data with optional filters
   * 
   * Query Parameter Building: Only includes non-empty filter values
   * This prevents sending unnecessary parameters and keeps URLs clean
   */
  getVaccines: async (filters: VaccineFilters = {}): Promise<VaccineListResponse> => {
    const params = new URLSearchParams();
    
    // Conditional Parameter Building: Only add non-empty filters
    if (filters.region) params.append('region', filters.region);
    if (filters.brand) params.append('brand', filters.brand);
    if (filters.year) params.append('year', filters.year.toString());
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.offset) params.append('offset', filters.offset.toString());

    const response = await apiClient.get<VaccineListResponse>(`/api/vaccines?${params.toString()}`);
    return response.data;
  },

  getSummary: async (filters: VaccineFilters = {}): Promise<SummaryResponse> => {
    const params = new URLSearchParams();
    if (filters.region) params.append('region', filters.region);
    if (filters.brand) params.append('brand', filters.brand);
    if (filters.year) params.append('year', filters.year.toString());

    const response = await apiClient.get<SummaryResponse>(`/api/summary?${params.toString()}`);
    return response.data;
  },

  chatQuery: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await apiClient.post<ChatResponse>('/api/ai/chat', request);
    return response.data;
  },

  /**
   * Get market predictions with enhanced error handling
   * 
   * Error Handling Strategy:
   * - Distinguishes between network errors and API errors
   * - Provides user-friendly error messages
   * - Re-throws for component-level error handling
   */
  getPredictions: async (
    filters: VaccineFilters = {},
    yearsAhead: number = 2
  ): Promise<PredictionResponse> => {
    try {
      const params = new URLSearchParams();
      if (filters.region) params.append('region', filters.region);
      if (filters.brand) params.append('brand', filters.brand);
      params.append('years_ahead', yearsAhead.toString());

      const response = await apiClient.get<PredictionResponse>(
        `/api/ai/predictions?${params.toString()}`
      );
      return response.data;
    } catch (error: any) {
      // Enhanced Error Handling: Provide actionable error messages
      // Network errors (no response) vs API errors (error response)
      if (error.request && !error.response) {
        throw new Error('Network error: Backend server is not reachable. Make sure the backend is running on port 8080.');
      }
      throw error;
    }
  },

  getRecommendations: async (filters: VaccineFilters = {}): Promise<Recommendation[]> => {
    const params = new URLSearchParams();
    if (filters.region) params.append('region', filters.region);
    if (filters.brand) params.append('brand', filters.brand);
    if (filters.year) params.append('year', filters.year.toString());

    const response = await apiClient.get<Recommendation[]>(
      `/api/ai/recommendations?${params.toString()}`
    );
    return response.data;
  },
};

