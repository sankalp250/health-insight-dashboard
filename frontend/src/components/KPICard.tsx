import { TrendingUp, DollarSign, Activity, BarChart3 } from 'lucide-react';
import type { SummaryKPI } from '../lib/api';

interface KPICardProps {
  kpi: SummaryKPI;
}

const iconMap: Record<string, React.ReactNode> = {
  'Total Market Size': <DollarSign className="w-6 h-6" />,
  'Average Price': <DollarSign className="w-6 h-6" />,
  'Total Doses Sold': <Activity className="w-6 h-6" />,
  'CAGR': <TrendingUp className="w-6 h-6" />,
};

export default function KPICard({ kpi }: KPICardProps) {
  const formatValue = (value: number, unit: string | null): string => {
    if (unit === 'USD') {
      if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
      if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
      if (value >= 1e3) return `$${(value / 1e3).toFixed(2)}K`;
      return `$${value.toFixed(2)}`;
    }
    if (unit === 'percent') {
      return `${value.toFixed(2)}%`;
    }
    if (unit === 'million doses') {
      return `${value.toFixed(2)}M`;
    }
    return value.toFixed(2);
  };

  const icon = iconMap[kpi.label] || <BarChart3 className="w-6 h-6" />;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg text-primary-600 dark:text-primary-400">
          {icon}
        </div>
      </div>
      <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
        {kpi.label}
      </h3>
      <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
        {formatValue(kpi.value, kpi.unit)}
      </p>
      {kpi.description && (
        <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">{kpi.description}</p>
      )}
    </div>
  );
}

