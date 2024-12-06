import axios from 'axios';
import authAxios from '@/services/api/setup'

const baseURL = import.meta.env.VITE_API_URL;

export async function fetchAuthenticatedUser() {
  try {
    const authToken = localStorage.getItem("authToken");
    console.log(authToken)

    const response = await authAxios.get(`${baseURL}/usermanagement/get-current-user`, {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    return response.data; 
  } catch (error) {
    console.error("Error fetching user:", error);
    return null;
  }
}
