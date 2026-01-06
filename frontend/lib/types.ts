// TypeScript types matching the backend schemas

export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent';
export type TaskCategory = 'work' | 'personal' | 'health' | 'finance' | 'education' | 'other';

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: TaskPriority;
  category: TaskCategory;
  due_date?: string; // ISO date string
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: TaskPriority;
  category?: TaskCategory;
  due_date?: string; // ISO date string
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  category?: TaskCategory;
  due_date?: string; // ISO date string
}

export interface TaskToggleComplete {
  completed: boolean;
}

export interface TaskFilterParams {
  status?: 'all' | 'pending' | 'completed';
  priority?: TaskPriority | 'all';
  category?: TaskCategory | 'all';
  sort?: 'created' | 'title' | 'due_date' | 'priority';
  page?: number;
  limit?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
}

export interface ErrorResponse {
  success: boolean;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

export interface TaskListResponse {
  success: boolean;
  data: Task[];
}

export interface TaskResponse {
  success: boolean;
  data: Task;
}

export interface User {
  id: string;
  email: string;
  name?: string;
  image?: string;
  email_verified?: string; // ISO date string
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface AuthResponse {
  success: boolean;
  data: {
    user: User;
    token: string;
  };
}