'use client';

import { Task } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Progress } from '../ui/progress';

interface TaskStatsProps {
  tasks: Task[];
}

export default function TaskStats({ tasks }: TaskStatsProps) {
  // Calculate statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Calculate by priority
  const urgentTasks = tasks.filter(task => task.priority === 'urgent' && !task.completed).length;
  const highTasks = tasks.filter(task => task.priority === 'high' && !task.completed).length;
  const mediumTasks = tasks.filter(task => task.priority === 'medium' && !task.completed).length;
  const lowTasks = tasks.filter(task => task.priority === 'low' && !task.completed).length;

  // Calculate by category
  const workTasks = tasks.filter(task => task.category === 'work' && !task.completed).length;
  const personalTasks = tasks.filter(task => task.category === 'personal' && !task.completed).length;
  const healthTasks = tasks.filter(task => task.category === 'health' && !task.completed).length;
  const financeTasks = tasks.filter(task => task.category === 'finance' && !task.completed).length;
  const educationTasks = tasks.filter(task => task.category === 'education' && !task.completed).length;
  const otherTasks = tasks.filter(task => task.category === 'other' && !task.completed).length;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* Total Tasks Card */}
      <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">{totalTasks}</div>
        </CardContent>
      </Card>

      {/* Completed Tasks Card */}
      <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">Completed</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-green-600 dark:text-green-400">{completedTasks}</div>
        </CardContent>
      </Card>

      {/* Pending Tasks Card */}
      <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">Pending</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{pendingTasks}</div>
        </CardContent>
      </Card>

      {/* Completion Rate Card */}
      <Card className="dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">Completion Rate</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{completionRate}%</div>
          <Progress value={completionRate} className="mt-2" />
        </CardContent>
      </Card>

      {/* Priority Breakdown */}
      <Card className="md:col-span-2 dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-gray-900 dark:text-white">Tasks by Priority</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Urgent</span>
              <span className="text-sm font-medium text-red-600 dark:text-red-400">{urgentTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">High</span>
              <span className="text-sm font-medium text-orange-600 dark:text-orange-400">{highTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Medium</span>
              <span className="text-sm font-medium text-yellow-600 dark:text-yellow-400">{mediumTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Low</span>
              <span className="text-sm font-medium text-green-600 dark:text-green-400">{lowTasks}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Category Breakdown */}
      <Card className="md:col-span-2 dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-gray-900 dark:text-white">Tasks by Category</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Work</span>
              <span className="text-sm font-medium text-blue-600 dark:text-blue-400">{workTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Personal</span>
              <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400">{personalTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Health</span>
              <span className="text-sm font-medium text-green-600 dark:text-green-400">{healthTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Finance</span>
              <span className="text-sm font-medium text-purple-600 dark:text-purple-400">{financeTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Education</span>
              <span className="text-sm font-medium text-cyan-600 dark:text-cyan-400">{educationTasks}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Other</span>
              <span className="text-sm font-medium text-gray-600 dark:text-gray-400">{otherTasks}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}