'use client';

import { useAuth } from '@/hooks/use-auth';
import MainLayout from '@/components/layout/main-layout';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import ProfileImageUpload from '@/components/auth/profile-image-upload';

export default function ProfilePage() {
  const { user, isLoading } = useAuth();

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
    return (
      <MainLayout>
        <div className="flex justify-center items-center h-64">
          <p>Please sign in to view your profile</p>
          <Link href="/login" className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Sign In
          </Link>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Profile</h1>

        <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-gray-900 dark:text-white">User Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="bg-gray-200 dark:bg-gray-700 rounded-full w-16 h-16 flex items-center justify-center">
                  {user.image ? (
                    <img
                      src={user.image}
                      alt="Profile"
                      className="w-full h-full rounded-full object-cover"
                    />
                  ) : (
                    <span className="text-xl font-semibold text-gray-700 dark:text-gray-300">
                      {user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                    </span>
                  )}
                </div>
                <div className="absolute bottom-0 right-0 bg-blue-500 rounded-full p-1 border-2 border-white dark:border-gray-800">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.121-1.121A2 2 0 0011.172 3H8.828a2 2 0 00-1.414.586L6.293 4.707A1 1 0 015.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
              <div>
                <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                  {user.name || user.email}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  {user.email}
                </p>
              </div>
            </div>

            <div className="mt-4">
              <ProfileImageUpload />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">User ID</label>
                <p className="text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-2 rounded-md">{user.id}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Created</label>
                <p className="text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-2 rounded-md">
                  {new Date(user.created_at).toLocaleDateString()}
                </p>
              </div>

              {user.updated_at && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Last Updated</label>
                  <p className="text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-2 rounded-md">
                    {new Date(user.updated_at).toLocaleDateString()}
                  </p>
                </div>
              )}

              {user.email_verified && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email Verified</label>
                  <p className="text-gray-900 dark:text-white bg-green-50 dark:bg-green-900/30 p-2 rounded-md text-green-800 dark:text-green-300">
                    {new Date(user.email_verified).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        <div className="mt-6 flex justify-end">
          <Link
            href="/tasks"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            Back to Tasks
          </Link>
        </div>
      </div>
    </MainLayout>
  );
}