<template>
    <div class="min-h-screen flex items-center justify-center">
      <p>Redirecting... Please wait.</p>
    </div>
  </template>
  
  <script>
  import { useRouter, useRoute } from "vue-router";
  
  export default {
    setup() {
      const router = useRouter();
      const route = useRoute();
  
      const processRedirect = () => {
        const token = route.query.token; // Retrieve the token from query parameters
        const userId = route.query.user_id; // Ensure you include this in your backend redirect
        
  
        if (token) {
          // Store the token and userId in localStorage for future API requests
          localStorage.setItem("authToken", token);
          console.log(localStorage.getItem("authToken"))
          localStorage.setItem("userId", userId);
  
          // Redirect the user to their respective dashboard based on their role
          const role = route.query.role; // Include role in your backend redirect URL
          if (role === "student") {
            router.push(`/students`);
          } else if (role === "professor") {
            router.push(`/professors`);
          } else if (role === "teacher_assistant") {
            router.push(`/tas`);
          } else if (role === "sds_coordinator") {
            router.push(`/sdscoordinators`);
          } else {
            router.push("/signin"); // Default fallback
          }
        } else {
          // Handle the failure case
          alert("Authentication failed. Please log in again.");
          router.push("/signin");
        }
      };
  
      // Process the redirect
      processRedirect();
    },
  };
  </script>
  