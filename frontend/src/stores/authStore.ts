import { defineStore } from 'pinia';
import { ref } from 'vue';
import { fetchAuthenticatedUser } from '@/services/api/auth';
import * as interfaces from '@/services/api/interfaces' 

export const useUserStore = defineStore('user', () => {
  const user = ref<interfaces.User>(null); // Holds the user state
  const isLoading = ref(false); // Holds if the user data is loading
  const error = ref(null); // Logs an error message, if any

  /**
   * Function to fetch the authenticated user data from the API
   * Logs an error if any
   */
  async function fetchUser() {
    isLoading.value = true;
    error.value = null;

    try {
      const userData = await fetchAuthenticatedUser() as interfaces.User;
      if (userData) {
        user.value = userData;
      } else {
        error.value = 'Failed to fetch user data.';
      }
    } catch (err) {
      error.value = 'An error occurred while fetching the user.';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Function to clear user data, on log out
   */
  function clearUser() {
    user.value = null;
    localStorage.removeItem('authToken');
  }

  /**
   * Function to get user ID
   */
  function getUserId() {
    if(user) {
        return user.value.user_ptr_id;
    }
    return;
  }

  /**
   * Automatically Update User Value
   */
  if (!user.value) {
    fetchUser();
  }

  return {
    user,
    isLoading,
    error,
    fetchUser,
    clearUser,
  };
});
