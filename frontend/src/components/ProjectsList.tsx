import React from 'react';
import { useProjectsByOrganization } from '../context/GraphQLContext';

interface ProjectsListProps {
  organizationId: number;
  onProjectSelect?: (projectId: number) => void;
}

const ProjectsList: React.FC<ProjectsListProps> = ({ organizationId, onProjectSelect }) => {
  const { loading, error, data } = useProjectsByOrganization(organizationId) as any;

  if (loading) return <div className="text-center py-8 text-slate-300">Loading projects...</div>;
  if (error) return <div className="text-red-300 text-center py-8">Error: {error.message}</div>;

  const projects = (data as any)?.projectsByOrganization || [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-blue-500/15 text-blue-100 border border-blue-500/30';
      case 'completed':
        return 'bg-emerald-500/15 text-emerald-100 border border-emerald-500/30';
      case 'on_hold':
        return 'bg-amber-500/15 text-amber-100 border border-amber-500/30';
      default:
        return 'bg-slate-500/15 text-slate-100 border border-slate-500/30';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">Projects</h2>
        <span className="text-sm text-slate-400">
          {projects.length} projects
        </span>
      </div>
      {projects.length === 0 ? (
        <div className="text-center py-8 text-slate-400">No projects found</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project: any) => (
            <div
              key={project.id}
              className="card-surface rounded-2xl p-6 hover:shadow-xl transition hover:-translate-y-1 cursor-pointer border border-white/5"
              onClick={() => onProjectSelect?.(Number(project.id))}
            >
              <div className="flex justify-between items-start mb-4">
                <div className="space-y-1">
                  <p className="text-xs uppercase tracking-[0.2em] text-blue-200">Project</p>
                  <h3 className="text-xl font-semibold text-white">{project.name}</h3>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(project.status)}`}>
                  {project.status}
                </span>
              </div>
              {project.description && (
                <p className="text-slate-300 text-sm mb-4 line-clamp-3">{project.description}</p>
              )}
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-slate-300">
                  <span>Tasks</span>
                  <span className="font-semibold text-white">{project.taskCount || 0}</span>
                </div>
                <div className="flex justify-between text-sm text-slate-300">
                  <span>Completed</span>
                  <span className="font-semibold text-emerald-200">{project.completedTaskCount || 0}</span>
                </div>
               
               
                {project.dueDate && (
                  <div className="text-xs text-slate-400 mt-2 flex items-center justify-between">
                    <span>Due</span>
                    <span className="text-slate-200">
                      {new Date(project.dueDate).toLocaleDateString()}
                    </span>
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
