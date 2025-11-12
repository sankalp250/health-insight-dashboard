import { useMemo } from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { VaccineRecord } from '../lib/api';

interface ChartsProps {
  data: VaccineRecord[];
}

const COLORS = ['#0ea5e9', '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef'];

export default function Charts({ data }: ChartsProps) {
  const marketSizeByRegion = useMemo(() => {
    const grouped = data.reduce((acc, record) => {
      acc[record.region] = (acc[record.region] || 0) + record.market_size_usd;
      return acc;
    }, {} as Record<string, number>);
    return Object.entries(grouped).map(([region, value]) => ({ region, value }));
  }, [data]);

  const marketSizeByBrand = useMemo(() => {
    const grouped = data.reduce((acc, record) => {
      acc[record.brand] = (acc[record.brand] || 0) + record.market_size_usd;
      return acc;
    }, {} as Record<string, number>);
    return Object.entries(grouped)
      .map(([brand, value]) => ({ brand, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 6);
  }, [data]);

  const timeSeriesData = useMemo(() => {
    const grouped = data.reduce((acc, record) => {
      const key = record.year;
      if (!acc[key]) {
        acc[key] = { year: key, marketSize: 0, doses: 0, avgPrice: 0, count: 0 };
      }
      acc[key].marketSize += record.market_size_usd;
      acc[key].doses += record.doses_sold_million;
      acc[key].avgPrice += record.avg_price_usd;
      acc[key].count += 1;
      return acc;
    }, {} as Record<number, { year: number; marketSize: number; doses: number; avgPrice: number; count: number }>);

    return Object.values(grouped)
      .map((item) => ({
        year: item.year,
        marketSize: item.marketSize / 1e6,
        doses: item.doses,
        avgPrice: item.avgPrice / item.count,
      }))
      .sort((a, b) => a.year - b.year);
  }, [data]);

  const growthByBrand = useMemo(() => {
    const grouped = data.reduce((acc, record) => {
      if (!acc[record.brand]) {
        acc[record.brand] = { brand: record.brand, totalGrowth: 0, count: 0 };
      }
      acc[record.brand].totalGrowth += record.growth_rate_percent;
      acc[record.brand].count += 1;
      return acc;
    }, {} as Record<string, { brand: string; totalGrowth: number; count: number }>);

    return Object.values(grouped)
      .map((item) => ({
        brand: item.brand,
        avgGrowth: item.totalGrowth / item.count,
      }))
      .sort((a, b) => b.avgGrowth - a.avgGrowth)
      .slice(0, 5);
  }, [data]);

  const regionDistribution = useMemo(() => {
    const grouped = data.reduce((acc, record) => {
      acc[record.region] = (acc[record.region] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    return Object.entries(grouped).map(([name, value]) => ({ name, value }));
  }, [data]);

  if (data.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500 dark:text-gray-400">
        No data available for the selected filters
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Market Size by Region - Bar Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Market Size by Region
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={marketSizeByRegion}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
            <XAxis dataKey="region" className="text-gray-600 dark:text-gray-400" />
            <YAxis className="text-gray-600 dark:text-gray-400" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
              formatter={(value: number) => [`$${(value / 1e6).toFixed(2)}M`, 'Market Size']}
            />
            <Legend />
            <Bar dataKey="value" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Time Series - Line Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Market Trends Over Time
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={timeSeriesData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
            <XAxis dataKey="year" className="text-gray-600 dark:text-gray-400" />
            <YAxis yAxisId="left" className="text-gray-600 dark:text-gray-400" />
            <YAxis yAxisId="right" orientation="right" className="text-gray-600 dark:text-gray-400" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="marketSize"
              stroke="#0ea5e9"
              strokeWidth={2}
              name="Market Size (M USD)"
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="doses"
              stroke="#8b5cf6"
              strokeWidth={2}
              name="Doses Sold (M)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Brands by Market Size */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Top Brands by Market Size
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={marketSizeByBrand} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
              <XAxis type="number" className="text-gray-600 dark:text-gray-400" />
              <YAxis dataKey="brand" type="category" className="text-gray-600 dark:text-gray-400" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
                formatter={(value: number) => [`$${(value / 1e6).toFixed(2)}M`, 'Market Size']}
              />
              <Legend />
              <Bar dataKey="value" fill="#6366f1" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Growth Rate by Brand */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Average Growth Rate by Brand
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={growthByBrand}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
              <XAxis dataKey="brand" className="text-gray-600 dark:text-gray-400" />
              <YAxis className="text-gray-600 dark:text-gray-400" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
                formatter={(value: number) => [`${value.toFixed(2)}%`, 'Avg Growth']}
              />
              <Legend />
              <Bar dataKey="avgGrowth" fill="#d946ef" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Region Distribution - Pie Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Data Distribution by Region
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={regionDistribution}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {regionDistribution.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

