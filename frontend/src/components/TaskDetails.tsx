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

  if (loading) return <div className="text-center py-8">Loading task details...</div>;
  if (error) return <div className="text-red-500 text-center py-8">Error: {error.message}</div>;

  const task = (data as any)?.task;

  if (!task) return null;

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

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addTaskComment({
        variables: {
          input: {
            taskId: task.id,
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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-2xl font-bold text-gray-800">{task.title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(task.status)}`}>
              {task.status}
            </span>
          </div>

          {task.description && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Description</h3>
              <p className="text-gray-600">{task.description}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 text-sm">
            {task.assigneeEmail && (
              <div>
                <span className="text-gray-500">Assignee:</span>
                <span className="ml-2 font-medium">{task.assigneeEmail}</span>
              </div>
            )}
            {task.dueDate && (
              <div>
                <span className="text-gray-500">Due Date:</span>
                <span className="ml-2 font-medium">
                  {new Date(task.dueDate).toLocaleString()}
                </span>
              </div>
            )}
            <div>
              <span className="text-gray-500">Created:</span>
              <span className="ml-2 font-medium">
                {new Date(task.createdAt).toLocaleString()}
              </span>
            </div>
            <div>
              <span className="text-gray-500">Comments:</span>
              <span className="ml-2 font-medium">{task.commentCount || 0}</span>
            </div>
          </div>

          <div className="border-t pt-4">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-lg font-semibold text-gray-800">Comments</h3>
              <button
                onClick={() => setShowCommentForm(!showCommentForm)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm"
              >
                + Add Comment
              </button>
            </div>

            {showCommentForm && (
              <form onSubmit={handleAddComment} className="mb-4 p-4 bg-gray-50 rounded-lg">
                <div className="mb-3">
                  <input
                    type="email"
                    placeholder="Your email"
                    value={commentAuthor}
                    onChange={(e) => setCommentAuthor(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2"
                  />
                </div>
                <div className="mb-3">
                  <textarea
                    placeholder="Write a comment..."
                    value={commentContent}
                    onChange={(e) => setCommentContent(e.target.value)}
                    required
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm"
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
                    className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}

            {task.comments && task.comments.length > 0 ? (
              <div className="space-y-3">
                {task.comments.map((comment: any) => (
                  <div key={comment.id} className="bg-gray-50 p-3 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <span className="font-medium text-gray-800">{comment.authorEmail}</span>
                      <span className="text-xs text-gray-500">
                        {new Date(comment.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm">{comment.content}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No comments yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskDetails;
