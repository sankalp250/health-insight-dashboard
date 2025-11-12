import { useState, useEffect } from 'react';
import { TrendingUp, Sparkles } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { vaccineApi } from '../lib/api';
import type { VaccineFilters } from '../lib/api';

interface PredictionsProps {
  filters: VaccineFilters;
}

export default function Predictions({ filters }: PredictionsProps) {
  const [predictions, setPredictions] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [yearsAhead, setYearsAhead] = useState(2);

  useEffect(() => {
    loadPredictions();
  }, [filters, yearsAhead]);

  const loadPredictions = async () => {
    try {
      setLoading(true);
      const data = await vaccineApi.getPredictions(filters, yearsAhead);
      setPredictions(data);
    } catch (error) {
      console.error('Failed to load predictions:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (!predictions || predictions.predictions.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <p className="text-gray-500 dark:text-gray-400">No predictions available.</p>
      </div>
    );
  }

  const chartData = predictions.predictions.map((pred: any) => ({
    year: pred.year,
    predicted: pred.predicted_market_size_usd / 1e6,
    lower: pred.confidence_interval_lower / 1e6,
    upper: pred.confidence_interval_upper / 1e6,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
            <TrendingUp className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Market Predictions
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Confidence: {(predictions.confidence * 100).toFixed(0)}% • Method: {predictions.method}
            </p>
          </div>
        </div>
        <select
          value={yearsAhead}
          onChange={(e) => setYearsAhead(parseInt(e.target.value))}
          className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
        >
          <option value={1}>1 year ahead</option>
          <option value={2}>2 years ahead</option>
          <option value={3}>3 years ahead</option>
          <option value={4}>4 years ahead</option>
          <option value={5}>5 years ahead</option>
        </select>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
          <XAxis dataKey="year" className="text-gray-600 dark:text-gray-400" />
          <YAxis className="text-gray-600 dark:text-gray-400" />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
            formatter={(value: number) => [`$${value.toFixed(2)}M`, 'Predicted Market Size']}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#0ea5e9"
            strokeWidth={2}
            name="Predicted Market Size (M USD)"
          />
          <Line
            type="monotone"
            dataKey="lower"
            stroke="#94a3b8"
            strokeDasharray="5 5"
            strokeWidth={1}
            name="Lower Bound"
          />
          <Line
            type="monotone"
            dataKey="upper"
            stroke="#94a3b8"
            strokeDasharray="5 5"
            strokeWidth={1}
            name="Upper Bound"
          />
        </LineChart>
      </ResponsiveContainer>

      {predictions.ai_insight && (
        <div className="mt-4 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg border border-primary-200 dark:border-primary-800">
          <div className="flex items-start gap-2">
            <Sparkles className="w-4 h-4 text-primary-600 dark:text-primary-400 mt-0.5 flex-shrink-0" />
            <p className="text-sm text-gray-700 dark:text-gray-300">{predictions.ai_insight}</p>
          </div>
        </div>
      )}

      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        {predictions.predictions.map((pred: any) => (
          <div
            key={pred.year}
            className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600"
          >
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{pred.year}</p>
            <p className="text-lg font-bold text-primary-600 dark:text-primary-400">
              ${(pred.predicted_market_size_usd / 1e6).toFixed(2)}M
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Price: ${pred.predicted_avg_price_usd.toFixed(2)} • Growth: {pred.predicted_growth_rate_percent.toFixed(2)}%
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

