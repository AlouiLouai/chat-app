import axios from 'axios';
import Cookies from 'js-cookie';  // Import js-cookie

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export class ProfileService {
  // Get Profile
  static async getProfile(): Promise<{ success: boolean; profile: any; message: string }> {
    try {
      const accessToken = Cookies.get('access_token'); // Retrieve the access token from cookies

      const response = await axios.get(`${API_BASE_URL}/user/profile`, {
        withCredentials: true, // Ensures cookies are included in the request
        headers: {
          Authorization: `Bearer ${accessToken}`, // Add the token to the Authorization header
        },
      });

      console.log('response : ', response);
      return response.data; // Includes success status, profile data, and message
    } catch (error: any) {
      console.error('Failed to fetch profile:', error.response?.data?.error || error.message);
      throw new Error(error.response?.data?.error || 'Failed to fetch profile');
    }
  }

  // Update Profile
  static async updateProfile(data: { [key: string]: any }, file?: File): Promise<{ success: boolean; message: string }> {
    try {
      const accessToken = Cookies.get('access_token'); // Retrieve the access token from cookies

      const formData = new FormData();
      Object.entries(data).forEach(([key, value]) => formData.append(key, value));
      if (file) {
        formData.append('file', file);
      }

      const response = await axios.put(`${API_BASE_URL}/user/profile`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${accessToken}`, // Add the token to the Authorization header
        },
        withCredentials: true, // Ensures cookies are included in the request
      });

      return response.data; // Includes success status and message
    } catch (error: any) {
      console.error('Failed to update profile:', error.response?.data?.error || error.message);
      throw new Error(error.response?.data?.error || 'Failed to update profile');
    }
  }
}
