import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
};

