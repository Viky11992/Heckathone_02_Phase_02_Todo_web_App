'use client';

import { useAuth } from '@/hooks/use-auth';
import { useRouter } from 'next/navigation';
import MainLayout from '@/components/layout/main-layout';
import Link from 'next/link';

export default function HomePage() {
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

  return (
    <MainLayout>
      <div className="max-w-3xl mx-auto text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">Welcome to Todo App</h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
          A simple and efficient task management application to help you stay organized.
        </p>

        {user ? (
          <div>
            <p className="text-gray-700 dark:text-gray-300 mb-6">Hello, {user.name || user.email}!</p>
            <Link
              href="/tasks"
              className="inline-block px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200"
            >
              View My Tasks
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-gray-700 dark:text-gray-300">Sign in to manage your tasks</p>
            <div className="flex flex-col sm:flex-row justify-center space-y-3 sm:space-y-0 sm:space-x-4">
              <Link
                href="/login"
                className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200"
              >
                Sign In
              </Link>
              <Link
                href="/signup"
                className="px-6 py-3 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-white font-medium rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors duration-200"
              >
                Sign Up
              </Link>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}