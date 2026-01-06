'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { useParams, useRouter } from 'next/navigation';
import { Task } from '@/lib/types';
import { api } from '@/lib/api';
import TaskForm from '@/components/task/task-form';
import MainLayout from '@/components/layout/main-layout';
import Link from 'next/link';

export default function TaskDetailPage() {
  const { id } = useParams();
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (user && id) {
      loadTask();
    }
  }, [user, id]);

  const loadTask = async () => {
    try {
      setLoading(true);
      setError(null);
      // The API call expects the task ID to be a number
      const taskId = Array.isArray(id) ? parseInt(id[0], 10) : parseInt(id, 10);
      const response = await api.getTask(user!.id, taskId);
      setTask(response.data);
    } catch (err: any) {
      setError(err.message || 'An error occurred while loading the task');
      console.error('Error loading task:', err);
    } finally {
      setLoading(false);
    }
  };

  if (isLoading || loading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center h-64">
          <p>Loading...</p>
        </div>
      </MainLayout>
    );
  }

  if (!user) {
    router.push('/login');
    return null;
  }

  if (error) {
    return (
      <MainLayout>
        <div className="max-w-2xl mx-auto p-4">
          <div className="p-4 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
          <Link href="/tasks" className="mt-4 inline-block text-blue-600 hover:underline">
            Back to Tasks
          </Link>
        </div>
      </MainLayout>
    );
  }

  if (!task) {
    return (
      <MainLayout>
        <div className="max-w-2xl mx-auto p-4">
          <div className="p-4 bg-yellow-100 text-yellow-700 rounded-md">
            Task not found
          </div>
          <Link href="/tasks" className="mt-4 inline-block text-blue-600 hover:underline">
            Back to Tasks
          </Link>
        </div>
      </MainLayout>
    );
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await api.deleteTask(user.id, task.id);
      router.push('/tasks');
    } catch (err: any) {
      setError(err.message || 'An error occurred while deleting the task');
      console.error('Error deleting task:', err);
    }
  };

  const handleToggleCompletion = async () => {
    try {
      await api.toggleTaskCompletion(user.id, task.id, { completed: !task.completed });
      // Reload the task to update the UI
      loadTask();
    } catch (err: any) {
      setError(err.message || 'An error occurred while updating the task');
      console.error('Error updating task:', err);
    }
  };

  return (
    <MainLayout>
      <div className="max-w-2xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Task Details</h1>
          <Link href="/tasks" className="text-blue-600 hover:underline">
            Back to Tasks
          </Link>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {isEditing ? (
          <TaskForm
            userId={user.id}
            task={{ id: task.id, title: task.title, description: task.description || '' }}
            onSuccess={() => {
              setIsEditing(false);
              loadTask(); // Reload the task to update the UI
            }}
            onCancel={() => setIsEditing(false)}
          />
        ) : (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex items-start">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggleCompletion}
                className="h-5 w-5 text-blue-600 rounded mt-1"
              />
              <div className="ml-4 flex-1">
                <h2 className={`text-xl font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {task.title}
                </h2>
                {task.description && (
                  <p className={`mt-3 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                    {task.description}
                  </p>
                )}
                <div className="mt-4 grid grid-cols-2 gap-4 text-sm text-gray-600">
                  <div>
                    <span className="font-medium">Created:</span>{' '}
                    {new Date(task.created_at).toLocaleString()}
                  </div>
                  <div>
                    <span className="font-medium">Updated:</span>{' '}
                    {new Date(task.updated_at).toLocaleString()}
                  </div>
                  <div>
                    <span className="font-medium">Status:</span>{' '}
                    <span className={task.completed ? 'text-green-600' : 'text-yellow-600'}>
                      {task.completed ? 'Completed' : 'Pending'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end space-x-3">
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Edit Task
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Delete Task
              </button>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}