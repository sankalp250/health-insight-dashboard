import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

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

export const vaccineApi = {
  getVaccines: async (filters: VaccineFilters = {}): Promise<VaccineListResponse> => {
    const params = new URLSearchParams();
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
      // If network error, return empty predictions with error message
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

