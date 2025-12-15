import { useState } from 'react';
import { GraphQLProvider } from './context/GraphQLContext';
import ProjectsList from './components/ProjectsList';
import ProjectStatistics from './components/ProjectStatistics';
import TasksList from './components/TasksList';
import TaskDetails from './components/TaskDetails';
import ProjectForm from './components/ProjectForm';
import OrganizationSelector from './components/OrganizationSelector';

function App() {
  const [organizationId, setOrganizationId] = useState<number | null>(null);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [editingProject, setEditingProject] = useState<any>(null);

  const handleProjectSelect = (projectId: number) => {
    setSelectedProjectId(projectId);
    setSelectedTaskId(null);
  };

  const handleTaskSelect = (taskId: number) => {
    setSelectedTaskId(taskId);
  };

  const handleCreateProject = () => {
    setEditingProject(null);
    setShowProjectForm(true);
  };

  return (
    <GraphQLProvider>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
                  Project Dashboard
                </h1>
                <p className="mt-1 text-xs sm:text-sm text-gray-500">
                  Select or create an organization to see its projects and progress.
                </p>
              </div>
              <button
                onClick={handleCreateProject}
                className="self-start sm:self-auto inline-flex items-center justify-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base disabled:opacity-50"
                disabled={!organizationId}
              >
                + New Project
              </button>
            </div>
            <OrganizationSelector
              value={organizationId}
              onChange={(id) => {
                setOrganizationId(id);
                setSelectedProjectId(null);
                setSelectedTaskId(null);
              }}
            />
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {showProjectForm && (
            <ProjectForm
              organizationId={organizationId as number}
              project={editingProject}
              onClose={() => {
                setShowProjectForm(false);
                setEditingProject(null);
              }}
              onSuccess={() => {
                setShowProjectForm(false);
                setEditingProject(null);
              }}
            />
          )}

          {selectedTaskId && (
            <TaskDetails
              taskId={selectedTaskId}
              onClose={() => setSelectedTaskId(null)}
            />
          )}

          <div className="space-y-8">
            {organizationId && (
              <ProjectStatistics organizationId={organizationId} />
            )}

            {selectedProjectId ? (
              <div className="space-y-6">
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => {
                      setSelectedProjectId(null);
                      setSelectedTaskId(null);
                    }}
                    className="text-blue-600 hover:text-blue-800 font-medium"
                  >
                    ← Back to Projects
                  </button>
                </div>
                <TasksList
                  projectId={selectedProjectId}
                  onTaskSelect={handleTaskSelect}
                />
              </div>
            ) : organizationId ? (
              <ProjectsList
                organizationId={organizationId}
                onProjectSelect={handleProjectSelect}
              />
            ) : null}
          </div>
        </main>
      </div>
    </GraphQLProvider>
  );
}

export default App;
