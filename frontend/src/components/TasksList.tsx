import React, { useState } from 'react';
import { useProject } from '../context/GraphQLContext';
import { useUpdateTask } from '../context/GraphQLContext';
import TaskForm from './TaskForm';

interface TasksListProps {
  projectId: number;
  onTaskSelect?: (taskId: number) => void;
}

const TasksList: React.FC<TasksListProps> = ({ projectId, onTaskSelect }) => {
  const { loading: projectLoading, error: projectError, data: projectData, refetch: refetchProject } = useProject(projectId);
  // const [createTask] = useCreateTask();
  const [updateTask] = useUpdateTask();
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);
  const [tasks] = useState<any[]>([]); 


  if (projectLoading) return <div className="text-center py-8">Loading project...</div>;
  if (projectError) return <div className="text-red-500 text-center py-8">Error: {projectError.message}</div>;

  const project = (projectData as any)?.project;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'done':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'todo':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    try {
      await updateTask({
        variables: {
          taskId,
          input: { status: newStatus },
        },
      });
      refetchProject();
  
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">
          Tasks - {project?.name}
        </h2>
        <div className="flex gap-2">
          <span className="text-sm text-gray-600 self-center">
            Total Tasks: {project?.taskCount || 0}
          </span>
          <button
            onClick={() => {
              setEditingTask(null);
              setShowTaskForm(true);
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
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
          onSuccess={() => {
            setShowTaskForm(false);
            setEditingTask(null);
            refetchProject();
          }}
        />
      )}

      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
        <p className="text-yellow-800 text-sm">
          <strong>Note:</strong> To display tasks, you need to add a <code>tasks_by_project</code> query to your GraphQL schema.
          Currently, tasks can be created and updated, but the list view requires a backend query.
        </p>
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No tasks found. Create a task to get started!</p>
          <p className="text-xs mt-2 text-gray-400">
            (Task list requires a tasks_by_project GraphQL query in the backend)
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task: any) => (
            <div
              key={task.id}
              className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow cursor-pointer border border-gray-200"
              onClick={() => onTaskSelect?.(task.id)}
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-800">{task.title}</h3>
                <select
                  value={task.status}
                  onChange={(e) => {
                    e.stopPropagation();
                    handleStatusChange(task.id, e.target.value);
                  }}
                  className={`px-3 py-1 rounded-full text-xs font-medium border-0 ${getStatusColor(task.status)}`}
                  onClick={(e) => e.stopPropagation()}
                >
                  <option value="todo">Todo</option>
                  <option value="in_progress">In Progress</option>
                  <option value="done">Done</option>
                </select>
              </div>
              {task.description && (
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">{task.description}</p>
              )}
              <div className="flex justify-between items-center text-sm">
                <div className="flex gap-4 text-gray-500">
                  {task.assigneeEmail && (
                    <span>Assignee: {task.assigneeEmail}</span>
                  )}
                  {task.dueDate && (
                    <span>Due: {new Date(task.dueDate).toLocaleDateString()}</span>
                  )}
                  {task.commentCount > 0 && (
                    <span>Comments: {task.commentCount}</span>
                  )}
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setEditingTask(task);
                    setShowTaskForm(true);
                  }}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
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
