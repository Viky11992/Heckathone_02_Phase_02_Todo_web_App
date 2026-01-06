'use client';

import { useAuth } from '@/hooks/use-auth';
import TaskForm from '@/components/task/task-form';
import MainLayout from '@/components/layout/main-layout';
import { useRouter } from 'next/navigation';

export default function CreateTaskPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  if (isLoading) {
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

  const handleSuccess = () => {
    router.push('/tasks');
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

  return (
    <MainLayout>
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">Create New Task</h1>
        <TaskForm
          userId={user.id}
          onSuccess={handleSuccess}
          onCancel={handleCancel}
        />
      </div>
    </MainLayout>
  );
}