<template>
    <div>
      <p v-if="loading">Processing your login...</p>
      <p v-else-if="error">Error: {{ error }}</p>
      <p v-else>Login successful! Redirecting...</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        loading: true,
        error: null,
      };
    },
    async mounted() {
      const { code, state, error } = this.$route.query;
  
      if (error) {
        this.error = error;
        this.loading = false;
        return;
      }
  
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/google-login/callback/", {
          params: { code, state },
          withCredentials: true,
        });
  
        // Save the user info and tokens (if needed)
        const user = response.data;
  
        // Redirect or update the state as needed
        this.$router.push("/students/1");
      } catch (err) {
        this.error = "Failed to complete the login process.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
  };
  </script>
  