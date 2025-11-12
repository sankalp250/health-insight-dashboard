/**
 * Main Application Component
 * 
 * Architecture Pattern: Container Component
 * - Manages global application state
 * - Orchestrates data fetching and state updates
 * - Handles side effects (theme, data loading)
 * 
 * State Management Strategy:
 * - Local state with React hooks (no external state management needed)
 * - Filters trigger automatic data refetch via useEffect
 * - Derived state for filter options extracted from data
 */

import { useState, useEffect } from 'react';
import { Menu, Moon, Sun } from 'lucide-react';
import Sidebar from './components/Sidebar';
import FilterPanel from './components/FilterPanel';
import KPICard from './components/KPICard';
import Charts from './components/Charts';
import AIChat from './components/AIChat';
import Predictions from './components/Predictions';
import { vaccineApi } from './lib/api';
import type { VaccineFilters, VaccineRecord, SummaryKPI } from './lib/api';

function App() {
  // UI State: Sidebar visibility and theme management
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [activeSection, setActiveSection] = useState('dashboard');
  
  // Data State: Filters and fetched data
  const [filters, setFilters] = useState<VaccineFilters>({});
  const [vaccineData, setVaccineData] = useState<VaccineRecord[]>([]);
  const [kpis, setKpis] = useState<SummaryKPI[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Derived State: Filter options extracted from data (prevents stale options)
  const [regions, setRegions] = useState<string[]>([]);
  const [brands, setBrands] = useState<string[]>([]);
  const [years, setYears] = useState<number[]>([]);

  // Side Effect: Theme Management
  // Applies/removes 'dark' class to document root for Tailwind dark mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Side Effect: Data Fetching
  // Automatically refetches data when filters change (reactive data loading)
  // This ensures UI always reflects current filter state
  useEffect(() => {
    loadData();
  }, [filters]);

  /**
   * Data Loading Function
   * 
   * Performance Optimization: Parallel API calls using Promise.all
   * - Fetches vaccines and summary simultaneously (reduces latency)
   * - Extracts filter options from data (single source of truth)
   * - Implements comprehensive error handling for different failure scenarios
   */
  const loadData = async () => {
    try {
      setLoading(true);
      
      // Parallel API Calls: Fetch both datasets simultaneously for better performance
      const [vaccinesResponse, summaryResponse] = await Promise.all([
        vaccineApi.getVaccines({ ...filters, limit: 500 }),
        vaccineApi.getSummary(filters),
      ]);

      // Update state with fetched data
      setVaccineData(vaccinesResponse.data);
      setKpis(summaryResponse.kpis);

      // Extract unique values for filter dropdowns
      // Using Set for O(1) uniqueness check, then sorting for UX
      const uniqueRegions = Array.from(new Set(vaccinesResponse.data.map((v) => v.region))).sort();
      const uniqueBrands = Array.from(new Set(vaccinesResponse.data.map((v) => v.brand))).sort();
      const uniqueYears = Array.from(new Set(vaccinesResponse.data.map((v) => v.year))).sort();

      // Lazy Initialization: Only set filter options once (prevents unnecessary re-renders)
      if (regions.length === 0) setRegions(uniqueRegions);
      if (brands.length === 0) setBrands(uniqueBrands);
      if (years.length === 0) setYears(uniqueYears);
    } catch (error: any) {
      // Error Handling: Categorize errors for better debugging
      console.error('Failed to load data:', error);
      
      if (error.response) {
        // Server responded with error status (4xx, 5xx)
        console.error('API Error:', error.response.status, error.response.data);
      } else if (error.request) {
        // Request made but no response (network issue)
        console.error('Network Error: Backend not reachable. Is it running on port 8080?');
      } else {
        // Request setup error
        console.error('Error:', error.message);
      }
    } finally {
      // Always reset loading state, even on error
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar 
        isOpen={sidebarOpen} 
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        activeSection={activeSection}
        onSectionChange={setActiveSection}
      />

      <div className="md:ml-64 transition-all">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-30">
          <div className="flex items-center justify-between px-4 py-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="md:hidden text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
            >
              <Menu className="w-6 h-6" />
            </button>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              Vaccine Market Analytics
            </h1>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </header>

        {/* Main Content */}
        <main className="p-4 md:p-6 lg:p-8">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          ) : (
            <>
              {/* Dashboard Section */}
              <section id="dashboard">
                {/* Filters */}
                <FilterPanel
                  filters={filters}
                  onFiltersChange={setFilters}
                  regions={regions}
                  brands={brands}
                  years={years}
                />

                {/* KPIs */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  {kpis.map((kpi) => (
                    <KPICard key={kpi.label} kpi={kpi} />
                  ))}
                </div>
              </section>

              {/* Analytics Section */}
              <section id="analytics" className="mt-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Analytics</h2>
                <Charts data={vaccineData} />
              </section>

              {/* Trends Section */}
              <section id="trends" className="mt-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Trends & Predictions</h2>
                <Predictions filters={filters} />
              </section>

              {/* Insights Section */}
              <section id="insights" className="mt-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">AI Insights</h2>
                <AIChat filters={filters} />
              </section>
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
