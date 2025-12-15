import React from 'react';
import { useProjectsByOrganization } from '../context/GraphQLContext';

interface ProjectsListProps {
  organizationId: number;
  onProjectSelect?: (projectId: number) => void;
}

const ProjectsList: React.FC<ProjectsListProps> = ({ organizationId, onProjectSelect }) => {
  const { loading, error, data } = useProjectsByOrganization(organizationId) as any;

  if (loading) return <div className="text-center py-8">Loading projects...</div>;
  if (error) return <div className="text-red-500 text-center py-8">Error: {error.message}</div>;

  const projects = (data as any)?.projectsByOrganization || [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'on_hold':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Projects</h2>
      {projects.length === 0 ? (
        <div className="text-center py-8 text-gray-500">No projects found</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project: any) => (
            <div
              key={project.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer border border-gray-200"
              onClick={() => onProjectSelect?.(project.id)}
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-xl font-semibold text-gray-800">{project.name}</h3>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                  {project.status}
                </span>
              </div>
              {project.description && (
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">{project.description}</p>
              )}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Tasks:</span>
                  <span className="font-medium">{project.taskCount || 0}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Completed:</span>
                  <span className="font-medium">{project.completedTaskCount || 0}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${project.completionRate || 0}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500 text-center mt-1">
                  {project.completionRate || 0}% Complete
                </div>
                {project.dueDate && (
                  <div className="text-xs text-gray-500 mt-2">
                    Due: {new Date(project.dueDate).toLocaleDateString()}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProjectsList;
