'use client';

import { useAuth } from '@/hooks/use-auth';
import MainLayout from '@/components/layout/main-layout';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useTheme } from '@/contexts/theme-context';
import DarkModeToggle from '@/components/common/dark-mode-toggle';

export default function SettingsPage() {
  const { user, isLoading, signOut } = useAuth();
  const { theme } = useTheme();

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
          <p>Please sign in to access settings</p>
          <Link href="/login" className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Sign In
          </Link>
        </div>
      </MainLayout>
    );
  }

  const handleSignOut = () => {
    signOut();
  };

  return (
    <MainLayout>
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Settings</h1>

        <div className="space-y-6">
          {/* Theme Settings */}
          <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900 dark:text-white">Appearance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-white">Dark Mode</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Switch between light and dark themes</p>
                </div>
                <DarkModeToggle />
              </div>
              <div className="mt-4 text-sm">
                <p className="text-gray-700 dark:text-gray-300">
                  Current theme: <span className="font-medium capitalize">{theme}</span>
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Account Settings */}
          <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900 dark:text-white">Account</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-white">Email</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{user.email}</p>
                </div>

                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-white">Account Created</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    {new Date(user.created_at).toLocaleDateString()}
                  </p>
                </div>

                <div className="pt-4">
                  <button
                    onClick={handleSignOut}
                    className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors duration-200"
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Application Info */}
          <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900 dark:text-white">Application</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Version</span>
                  <span className="text-sm text-gray-900 dark:text-white">1.0.0</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Last Updated</span>
                  <span className="text-sm text-gray-900 dark:text-white">January 2026</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="mt-6 flex justify-end space-x-3">
          <Link
            href="/profile"
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors duration-200"
          >
            Profile
          </Link>
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