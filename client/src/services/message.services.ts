import axios from 'axios';
import Cookies from 'js-cookie';  // Import js-cookie

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export class MessageService {
  // Get Messages
  static async getMessages(): Promise<{ messages: [{message: string, username: string}]}> {
    try {
        const accessToken = Cookies.get('access_token');

        const response = await axios.get(`${API_BASE_URL}/message/messages`, {
            withCredentials: true,
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        })
        return response.data;
    } catch (error: any) {
        console.error('Failed to fetch messages:', error.response?.data?.error || error.message);
        throw new Error(error.response?.data?.error || 'Failed to fetch messages'); 
    }
  }
}
