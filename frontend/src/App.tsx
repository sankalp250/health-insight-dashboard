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
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [filters, setFilters] = useState<VaccineFilters>({});
  const [vaccineData, setVaccineData] = useState<VaccineRecord[]>([]);
  const [kpis, setKpis] = useState<SummaryKPI[]>([]);
  const [loading, setLoading] = useState(true);
  const [regions, setRegions] = useState<string[]>([]);
  const [brands, setBrands] = useState<string[]>([]);
  const [years, setYears] = useState<number[]>([]);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [vaccinesResponse, summaryResponse] = await Promise.all([
        vaccineApi.getVaccines({ ...filters, limit: 500 }),
        vaccineApi.getSummary(filters),
      ]);

      setVaccineData(vaccinesResponse.data);
      setKpis(summaryResponse.kpis);

      // Extract unique values for filters
      const uniqueRegions = Array.from(new Set(vaccinesResponse.data.map((v) => v.region))).sort();
      const uniqueBrands = Array.from(new Set(vaccinesResponse.data.map((v) => v.brand))).sort();
      const uniqueYears = Array.from(new Set(vaccinesResponse.data.map((v) => v.year))).sort();

      if (regions.length === 0) setRegions(uniqueRegions);
      if (brands.length === 0) setBrands(uniqueBrands);
      if (years.length === 0) setYears(uniqueYears);
    } catch (error: any) {
      console.error('Failed to load data:', error);
      // Show error to user
      if (error.response) {
        console.error('API Error:', error.response.status, error.response.data);
      } else if (error.request) {
        console.error('Network Error: Backend not reachable. Is it running on port 8080?');
      } else {
        console.error('Error:', error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

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

              {/* Charts */}
              <Charts data={vaccineData} />

              {/* AI Features Section */}
              <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
                <AIChat filters={filters} />
                <Predictions filters={filters} />
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
