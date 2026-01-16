// Auth service to handle authentication with backend
// This service will generate and validate tokens with the backend API

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://vickey92-todo-backend.hf.space/api';

class AuthService {
  // Generate a new JWT token from the backend
  async generateToken(userData: { user_id: string; email?: string; name?: string }) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/generate-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Token generation failed: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error generating token:', error);
      throw error;
    }
  }

  // Validate an existing token with the backend
  async validateToken(token: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/validate-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      });

      if (!response.ok) {
        return { success: false };
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error validating token:', error);
      return { success: false };
    }
  }

  // Store token and user data in localStorage
  setAuthData(token: string, userId: string, email: string) {
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user_id', userId);
    localStorage.setItem('user_email', email);
  }

  // Get token from localStorage
  getAuthToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  // Get user ID from localStorage
  getUserId(): string | null {
    return localStorage.getItem('user_id');
  }

  // Clear authentication data
  clearAuthData() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    const token = this.getAuthToken();
    return !!token;
  }
}

// Export a singleton instance
export const authService = new AuthService();
export default authService;