import { Filter, Home, TrendingUp, BarChart3, PieChart } from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  activeSection?: string;
  onSectionChange?: (section: string) => void;
}

export default function Sidebar({ isOpen, onToggle, activeSection = 'dashboard', onSectionChange }: SidebarProps) {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>, section: string) => {
    e.preventDefault();
    if (onSectionChange) {
      onSectionChange(section);
    }
    // Scroll to section
    const element = document.getElementById(section);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <aside
      className={`fixed left-0 top-0 h-full bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-transform duration-300 z-40 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      } md:translate-x-0 w-64`}
    >
      <div className="flex flex-col h-full p-4">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-xl font-bold text-primary-600 dark:text-primary-400">
            Health Insight
          </h1>
          <button
            onClick={onToggle}
            className="md:hidden text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100"
          >
            <Filter className="w-5 h-5" />
          </button>
        </div>

        <nav className="flex-1 space-y-2">
          <a
            href="#dashboard"
            onClick={(e) => handleClick(e, 'dashboard')}
            className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
              activeSection === 'dashboard'
                ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <Home className="w-5 h-5" />
            <span>Dashboard</span>
          </a>
          <a
            href="#analytics"
            onClick={(e) => handleClick(e, 'analytics')}
            className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
              activeSection === 'analytics'
                ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <BarChart3 className="w-5 h-5" />
            <span>Analytics</span>
          </a>
          <a
            href="#trends"
            onClick={(e) => handleClick(e, 'trends')}
            className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
              activeSection === 'trends'
                ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <TrendingUp className="w-5 h-5" />
            <span>Trends</span>
          </a>
          <a
            href="#insights"
            onClick={(e) => handleClick(e, 'insights')}
            className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
              activeSection === 'insights'
                ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <PieChart className="w-5 h-5" />
            <span>Insights</span>
          </a>
        </nav>
      </div>
    </aside>
  );
}

