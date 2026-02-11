import React, { useState } from "react";
import { useProject, useTasksByProject } from "../context/GraphQLContext";
import { useUpdateTask } from "../context/GraphQLContext";
import TaskForm from "./TaskForm";

interface TasksListProps {
  projectId: number;
  onTaskSelect?: (taskId: number) => void;
}

const TasksList: React.FC<TasksListProps> = ({ projectId, onTaskSelect }) => {
  const {
    loading: projectLoading,
    error: projectError,
    data: projectData,
    refetch: refetchProject,
  } = useProject(projectId);
  const {
    loading: tasksLoading,
    error: tasksError,
    data: tasksData,
    refetch: refetchTasks,
  } = useTasksByProject(projectId);

  const [updateTask] = useUpdateTask();
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);

  if (projectLoading || tasksLoading)
    return <div className="text-center py-8 text-slate-300">Loading...</div>;
  if (projectError || tasksError)
    return (
      <div className="text-red-300 text-center py-8">
        Error: {projectError?.message || tasksError?.message}
      </div>
    );

  const project = (projectData as any)?.project;
  const tasks = (tasksData as any)?.tasksByProject || [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "done":
        return "bg-emerald-500/15 text-emerald-100 border border-emerald-500/30";
      case "in_progress":
        return "bg-blue-500/15 text-blue-100 border border-blue-500/30";
      case "todo":
        return "bg-amber-500/15 text-amber-100 border border-amber-500/30";
      default:
        return "bg-slate-500/15 text-slate-100 border border-slate-500/30";
    }
  };

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    try {
      await updateTask({
        variables: {
          taskId: Number(taskId),
          input: { status: newStatus },
        },
      });
      refetchTasks();
    } catch (err) {
      console.error("Error updating task:", err);
    }
  };

  const handleSuccess = () => {
    setShowTaskForm(false);
    setEditingTask(null);
    refetchProject();
    refetchTasks();
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-blue-200">
            Tasks
          </p>
          <h2 className="text-2xl font-bold text-white">{project?.name}</h2>
          <p className="text-sm text-slate-400">
            Manage execution, unblock owners, and keep momentum high.
          </p>
        </div>
        <div className="flex gap-3 items-center">
          <span className="text-sm text-slate-300 self-center">
            Total Tasks: <strong className="text-white">{tasks.length}</strong>
          </span>
          <button
            onClick={() => {
              setEditingTask(null);
              setShowTaskForm(true);
            }}
            className="bg-white text-slate-900 px-4 py-2 rounded-xl font-semibold shadow-lg shadow-blue-900/30 hover:-translate-y-0.5 transition"
          >
            + Add Task
          </button>
        </div>
      </div>

      {showTaskForm && (
        <TaskForm
          projectId={projectId}
          task={editingTask}
          onClose={() => {
            setShowTaskForm(false);
            setEditingTask(null);
          }}
          onSuccess={handleSuccess}
        />
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          <p>No tasks found. Create a task to get started!</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task: any) => (
            <div
              key={task.id}
              className="card-surface rounded-xl p-4 hover:shadow-xl transition hover:-translate-y-0.5 cursor-pointer border border-white/5"
              onClick={() => onTaskSelect?.(Number(task.id))}
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-white">
                  {task.title}
                </h3>
                <select
                  value={task.status}
                  onChange={(e) => {
                    e.stopPropagation();
                    handleStatusChange(task.id, e.target.value);
                  }}
                  className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusColor(task.status)}`}
                  onClick={(e) => e.stopPropagation()}
                >
                  <option value="todo">Todo</option>
                  <option value="in_progress">In Progress</option>
                  <option value="done">Done</option>
                </select>
              </div>
              {task.description && (
                <p className="text-slate-300 text-sm mb-3 line-clamp-2">
                  {task.description}
                </p>
              )}
              <div className="flex justify-between items-center text-sm">
                <div className="flex gap-4 text-slate-400">
                  {task.assigneeEmail && (
                    <span>
                      Assignee:{" "}
                      <span className="text-slate-200">
                        {task.assigneeEmail}
                      </span>
                    </span>
                  )}
                  {task.dueDate && (
                    <span>
                      Due:{" "}
                      <span className="text-slate-200">
                        {new Date(task.dueDate).toLocaleDateString()}
                      </span>
                    </span>
                  )}
                  {task.commentCount > 0 && (
                    <span>
                      Comments:{" "}
                      <span className="text-slate-200">
                        {task.commentCount}
                      </span>
                    </span>
                  )}
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setEditingTask(task);
                    setShowTaskForm(true);
                  }}
                  className="text-blue-200 hover:text-white text-sm font-semibold"
                >
                  Edit
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TasksList;
