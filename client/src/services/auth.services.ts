import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export class AuthService {
  // User Registration
  static async register(userData: RegisterData): Promise<{ message: string; user: { username: string; email: string } }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
      return response.data; // Includes success message and user data
    } catch (error: any) {
      console.error('Registration failed:', error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  // User Login
  static async login(credentials: LoginCredentials): Promise<Tokens> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
      return response.data; // Includes access and refresh tokens
    } catch (error: any) {
      console.error('Login failed:', error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  // User Logout
  static async logout(refreshToken: string): Promise<{ message: string }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/logout`, { refresh_token: refreshToken });
      return response.data; // Includes success message
    } catch (error: any) {
      console.error('Logout failed:', error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || 'Logout failed');
    }
  }

  // Forgot Password
  static async forgotPassword(email: ForgotPasswordData): Promise<{ message: string }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/forgot-password`, email);
      console.log('response from forgot password :', {response})
      return response.data; // Includes success or failure message
    } catch (error: any) {
      console.error('Forgot password request failed:', error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || 'Forgot password request failed');
    }
  }

  // Reset Password
  static async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/reset-password/${token}`, { new_password: newPassword });
      return response.data; // Includes success or failure message
    } catch (error: any) {
      console.error('Password reset failed:', error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || 'Password reset failed');
    }
  }
}
