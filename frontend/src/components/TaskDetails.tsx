import React, { useState } from 'react';
import { useTask } from '../context/GraphQLContext';
import { useAddTaskComment } from '../context/GraphQLContext';

interface TaskDetailsProps {
  taskId: number;
  onClose: () => void;
}

const TaskDetails: React.FC<TaskDetailsProps> = ({ taskId, onClose }) => {
  const { loading, error, data, refetch } = useTask(taskId) as any;
  const [addTaskComment] = useAddTaskComment();
  const [commentContent, setCommentContent] = useState('');
  const [commentAuthor, setCommentAuthor] = useState('');
  const [showCommentForm, setShowCommentForm] = useState(false);

  if (loading) return <div className="text-center py-8 text-slate-300">Loading task details...</div>;
  if (error) return <div className="text-red-300 text-center py-8">Error: {error.message}</div>;

  const normalizeStatus = (status?: string) =>
    status ? status.toLowerCase() : status;

  const task = (data as any)?.task
    ? { ...(data as any).task, status: normalizeStatus((data as any).task.status) }
    : null;

  if (!task) return null;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'done':
        return 'bg-emerald-500/15 text-emerald-100 border border-emerald-500/30';
      case 'in_progress':
        return 'bg-blue-500/15 text-blue-100 border border-blue-500/30';
      case 'todo':
        return 'bg-amber-500/15 text-amber-100 border border-amber-500/30';
      default:
        return 'bg-slate-500/15 text-slate-100 border border-slate-500/30';
    }
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addTaskComment({
        variables: {
          input: {
            taskId: Number(task.id),
            content: commentContent,
            authorEmail: commentAuthor,
          },
        },
      });
      setCommentContent('');
      setCommentAuthor('');
      setShowCommentForm(false);
      refetch();
    } catch (err) {
      console.error('Error adding comment:', err);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="card-surface rounded-2xl shadow-2xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto border border-white/10">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-2xl font-bold text-white">{task.title}</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-2xl"
          >
            ×
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${getStatusColor(task.status)}`}>
              {task.status}
            </span>
          </div>

          {task.description && (
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Description</h3>
              <p className="text-slate-300">{task.description}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 text-sm">
            {task.assigneeEmail && (
              <div>
                <span className="text-slate-400">Assignee:</span>
                <span className="ml-2 font-semibold text-white">{task.assigneeEmail}</span>
              </div>
            )}
            {task.dueDate && (
              <div>
                <span className="text-slate-400">Due Date:</span>
                <span className="ml-2 font-semibold text-white">
                  {new Date(task.dueDate).toLocaleString()}
                </span>
              </div>
            )}
            <div>
              <span className="text-slate-400">Created:</span>
              <span className="ml-2 font-semibold text-white">
                {new Date(task.createdAt).toLocaleString()}
              </span>
            </div>
            <div>
              <span className="text-slate-400">Comments:</span>
              <span className="ml-2 font-semibold text-white">{task.commentCount || 0}</span>
            </div>
          </div>

          <div className="border-t pt-4">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-lg font-semibold text-white">Comments</h3>
              <button
                onClick={() => setShowCommentForm(!showCommentForm)}
                className="bg-white text-slate-900 px-4 py-2 rounded-lg font-semibold hover:-translate-y-0.5 transition text-sm"
              >
                + Add Comment
              </button>
            </div>

            {showCommentForm && (
              <form onSubmit={handleAddComment} className="mb-4 p-4 bg-slate-900 rounded-lg border border-white/10">
                <div className="mb-3">
                  <input
                    type="email"
                    placeholder="Your email"
                    value={commentAuthor}
                    onChange={(e) => setCommentAuthor(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-slate-700 rounded-lg mb-2 bg-slate-800 text-white"
                  />
                </div>
                <div className="mb-3">
                  <textarea
                    placeholder="Write a comment..."
                    value={commentContent}
                    onChange={(e) => setCommentContent(e.target.value)}
                    required
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-700 rounded-lg bg-slate-800 text-white"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-500 text-sm"
                  >
                    Post Comment
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowCommentForm(false);
                      setCommentContent('');
                      setCommentAuthor('');
                    }}
                    className="bg-slate-700 text-white px-4 py-2 rounded-lg hover:bg-slate-600 text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}

            {task.comments && task.comments.length > 0 ? (
              <div className="space-y-3">
                {task.comments.map((comment: any) => (
                  <div key={comment.id} className="bg-slate-900 p-3 rounded-lg border border-white/10">
                    <div className="flex justify-between items-start mb-2">
                      <span className="font-semibold text-white">{comment.authorEmail}</span>
                      <span className="text-xs text-slate-400">
                        {new Date(comment.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <p className="text-slate-200 text-sm">{comment.content}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-400 text-sm">No comments yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskDetails;
