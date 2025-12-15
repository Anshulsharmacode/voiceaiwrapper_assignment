import React from 'react';
import { useProjectStatistics } from '../context/GraphQLContext';

interface ProjectStatisticsProps {
  organizationId: number;
}

const ProjectStatistics: React.FC<ProjectStatisticsProps> = ({ organizationId }) => {
  const { loading, error, data } = useProjectStatistics(organizationId) as any;

  if (loading) return <div className="text-center py-4">Loading statistics...</div>;
  if (error) return <div className="text-red-500 text-center py-4">Error: {error.message}</div>;

  const stats = data?.projectStatistics as any;

  if (!stats) return null;

  const StatCard = ({ title, value, color = 'blue' }: { title: string; value: number | string; color?: string }) => {
    const colorClasses = {
      blue: 'bg-blue-500',
      green: 'bg-green-500',
      yellow: 'bg-yellow-500',
      purple: 'bg-purple-500',
      red: 'bg-red-500',
    };

    return (
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <div className={`${colorClasses[color as keyof typeof colorClasses]} w-12 h-12 rounded-lg flex items-center justify-center mb-3`}>
          <span className="text-white text-2xl font-bold">{value}</span>
        </div>
        <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
      </div>
    );
  };

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Statistics</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <StatCard title="Total Projects" value={stats.totalProjects} color="blue" />
        <StatCard title="Active" value={stats.activeProjects} color="green" />
        <StatCard title="Completed" value={stats.completedProjects} color="purple" />
        <StatCard title="On Hold" value={stats.onHoldProjects} color="yellow" />
        <StatCard title="Total Tasks" value={stats.totalTasks} color="red" />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <StatCard title="Completed Tasks" value={stats.completedTasks} color="green" />
        <StatCard title="In Progress" value={stats.inProgressTasks} color="blue" />
        <StatCard title="Todo" value={stats.todoTasks} color="yellow" />
      </div>
      <div className="mt-6 bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Overall Completion Rate</h3>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className="bg-green-600 h-4 rounded-full transition-all flex items-center justify-center"
            style={{ width: `${stats.overallCompletionRate || 0}%` }}
          >
            <span className="text-white text-xs font-medium">
              {stats.overallCompletionRate?.toFixed(1) || 0}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectStatistics;
