'use client';

import React, { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { User } from '@/lib/types';
import { authService } from '@/lib/auth-service';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  forgotPassword: (email: string) => Promise<void>;
  updateProfileImage: (image: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType>(undefined!);

// Better Auth integration - now connects to our backend auth endpoints
const betterAuthAPI = {
  async signIn(email: string, password: string): Promise<{ user: User; token: string }> {
    // In a real implementation, this would call the Better Auth API
    // For now, we'll generate a token using our backend auth service
    await new Promise(resolve => setTimeout(resolve, 500));

    if (email && password) {
      // Generate a consistent user ID based on email to ensure tasks persist across sessions
      const userId = `user-${btoa(email).replace(/[^a-zA-Z0-9]/g, '')}`;

      // Generate token using backend service
      const tokenResponse = await authService.generateToken({
        user_id: userId,
        email,
        name: email.split('@')[0]
      });

      if (!tokenResponse.success) {
        throw new Error('Failed to generate authentication token');
      }

      const mockUser: User = {
        id: userId,
        email,
        name: email.split('@')[0],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      // Store auth data using the auth service
      authService.setAuthData(tokenResponse.token, userId, email);

      return { user: mockUser, token: tokenResponse.token };
    }

    throw new Error('Invalid credentials');
  },

  async signUp(email: string, password: string): Promise<{ user: User; token: string }> {
    // In a real implementation, this would call the Better Auth API
    // For now, we'll generate a token using our backend auth service
    await new Promise(resolve => setTimeout(resolve, 500));

    if (email && password.length >= 6) {
      // Generate a consistent user ID based on email to ensure tasks persist across sessions
      const userId = `user-${btoa(email).replace(/[^a-zA-Z0-9]/g, '')}`;

      // Generate token using backend service
      const tokenResponse = await authService.generateToken({
        user_id: userId,
        email,
        name: email.split('@')[0]
      });

      if (!tokenResponse.success) {
        throw new Error('Failed to generate authentication token');
      }

      const mockUser: User = {
        id: userId,
        email,
        name: email.split('@')[0],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      // Store auth data using the auth service
      authService.setAuthData(tokenResponse.token, userId, email);

      return { user: mockUser, token: tokenResponse.token };
    }

    throw new Error('Invalid registration data');
  },

  async signOut(): Promise<void> {
    // In a real implementation, this would call the Better Auth API
    // For now, we'll simulate the API call
    await new Promise(resolve => setTimeout(resolve, 300));

    // Remove token from localStorage using auth service
    authService.clearAuthData();
  },

  async forgotPassword(email: string): Promise<void> {
    // In a real implementation, this would call the Better Auth API
    // For now, we'll simulate the API call
    await new Promise(resolve => setTimeout(resolve, 500));

    // In a real app, this would send a password reset email via Better Auth
    console.log(`Password reset requested for: ${email}`);
  }
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on initial load
    const initAuth = async () => {
      try {
        // Use auth service to check if user is authenticated
        if (authService.isAuthenticated()) {
          const token = authService.getAuthToken();
          const userId = authService.getUserId();
          const email = localStorage.getItem('user_email') || 'user@example.com';

          if (token && userId) {
            // Validate token with backend
            const validation = await authService.validateToken(token);

            if (validation.success) {
              const mockUser: User = {
                id: userId,
                email: email,
                name: email.split('@')[0],
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString(),
              };
              setUser(mockUser);
            } else {
              // Token is invalid, clear auth data
              authService.clearAuthData();
            }
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const result = await betterAuthAPI.signIn(email, password);
      setUser(result.user);
    } catch (error) {
      throw error;
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const result = await betterAuthAPI.signUp(email, password);
      setUser(result.user);
    } catch (error) {
      throw error;
    }
  };

  const signOut = async () => {
    try {
      await betterAuthAPI.signOut();
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const forgotPassword = async (email: string) => {
    try {
      await betterAuthAPI.forgotPassword(email);
    } catch (error) {
      throw error;
    }
  };

  const updateProfileImage = async (image: string) => {
    if (!user) return;

    try {
      // Update the user's profile image in the backend
      // await api.updateProfileImage(user.id, image);

      // For now, we'll update the user object in state
      // In a real implementation, you would update the backend and then update the state
      const updatedUser: User = {
        ...user,
        image: image,
        updated_at: new Date().toISOString()
      };

      setUser(updatedUser);

      // In a real implementation, you would also update the user in localStorage
    } catch (error) {
      console.error('Error updating profile image:', error);
      throw error;
    }
  };

  const authValue = {
    user,
    isLoading,
    signIn,
    signUp,
    signOut,
    forgotPassword,
    updateProfileImage
  };

  return React.createElement(AuthContext.Provider, { value: authValue }, children);
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};