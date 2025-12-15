import { useMemo, useState } from "react";
import { GraphQLProvider } from "./context/GraphQLContext";
import ProjectsList from "./components/ProjectsList";
// import ProjectStatistics from "./components/ProjectStatistics";
import TasksList from "./components/TasksList";
import TaskDetails from "./components/TaskDetails";
import ProjectForm from "./components/ProjectForm";
import OrganizationSelector from "./components/OrganizationSelector";

function App() {
  const [organizationId, setOrganizationId] = useState<number | null>(null);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(
    null
  );
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [editingProject, setEditingProject] = useState<any>(null);

  const heroSummary = useMemo(() => {
    if (!organizationId) {
      return "Pick an organization to see projects, tasks, and momentum.";
    }
    if (selectedProjectId) {
      return "You’re focusing this workspace on a single project. Jump into tasks or details below.";
    }
    return "Explore all projects for this organization, track progress, and launch new work quickly.";
  }, [organizationId, selectedProjectId]);

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
      <div className="min-h-screen text-slate-100">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute -top-24 -left-10 h-72 w-72 rounded-full bg-blue-600/30 blur-3xl" />
          <div className="absolute top-10 right-0 h-64 w-64 rounded-full bg-indigo-600/25 blur-3xl" />
        </div>

        <header className="relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
            <div className="glass-surface rounded-3xl p-6 sm:p-8 border border-white/10 overflow-hidden">
              <div className="absolute inset-y-0 right-0 w-1/3 bg-gradient-to-l from-indigo-600/15 via-slate-900/0 to-transparent pointer-events-none" />
              <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between relative">
                <div className="space-y-3">
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/15 text-xs uppercase tracking-[0.2em] text-blue-100">
                    Task HQ
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    Live
                  </div>
                  <div className="space-y-2">
                    <h1 className="text-3xl sm:text-4xl font-bold">
                      Ship tasks with clarity and momentum
                    </h1>
                    <p className="text-sm sm:text-base text-slate-200 max-w-2xl">
                      {heroSummary}
                    </p>
                  </div>
                  <div className="flex flex-col sm:flex-row gap-3">
                    <button
                      onClick={handleCreateProject}
                      className="inline-flex items-center justify-center px-4 py-3 rounded-xl bg-gradient-to-r from-white to-slate-100 text-slate-900 font-semibold shadow-lg shadow-blue-900/30 hover:-translate-y-0.5 transition duration-200 disabled:opacity-60"
                      disabled={!organizationId}
                    >
                      + New Project
                    </button>
                    <button
                      onClick={() => {
                        setSelectedProjectId(null);
                        setSelectedTaskId(null);
                      }}
                      className="inline-flex items-center justify-center px-4 py-3 rounded-xl border border-white/20 text-slate-100 hover:bg-white/5 transition duration-200"
                    >
                      Reset View
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12 z-10">
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

          <div className="grid gap-6 w-full flex relative">
            <div className="space-y-6">
              <div className="card-surface rounded-2xl p-5">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                  <div>
                    <p className="text-xs uppercase tracking-[0.2em] text-blue-200">
                      Organization
                    </p>
                    <p className="text-sm text-slate-300">
                      Switch context or create a new workspace.
                    </p>
                  </div>
                  <div className="w-full sm:w-auto sm:min-w-[320px]">
                    <OrganizationSelector
                      value={organizationId}
                      onChange={(id) => {
                        setOrganizationId(id);
                        setSelectedProjectId(null);
                        setSelectedTaskId(null);
                      }}
                    />
                  </div>
                </div>
              </div>
{/* 
              {organizationId && (
                <ProjectStatistics organizationId={organizationId} />
              )} */}

              <div className="card-surface rounded-2xl p-5">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-xs uppercase tracking-[0.2em] text-blue-200">
                      Execution
                    </p>
                    <h2 className="text-xl font-semibold">
                      {selectedProjectId ? "Task Board" : "Project Portfolio"}
                    </h2>
                  </div>
                  {selectedProjectId && (
                    <button
                      onClick={() => {
                        setSelectedProjectId(null);
                        setSelectedTaskId(null);
                      }}
                      className="text-blue-200 hover:text-white text-sm font-medium"
                    >
                      ← Back to projects
                    </button>
                  )}
                </div>

                {selectedProjectId ? (
                  <TasksList
                    projectId={selectedProjectId}
                    onTaskSelect={handleTaskSelect}
                  />
                ) : organizationId ? (
                  <ProjectsList
                    organizationId={organizationId}
                    onProjectSelect={handleProjectSelect}
                  />
                ) : (
                  <div className="text-center text-slate-400 py-10">
                    Select an organization to view projects.
                  </div>
                )}
              </div>
            </div>

         
          </div>
        </main>
      </div>
    </GraphQLProvider>
  );
}

export default App;
