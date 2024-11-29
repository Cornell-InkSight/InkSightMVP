<template>
    <div class="flex h-screen]">
      <!-- Sidebar -->
      <aside class="w-[100%] bg-gray-100 shadow-md flex flex-col">
        <!-- Header -->
        <div class="p-4">
          <button class="bg-blue-500 text-white px-4 py-2 rounded-lg w-full">
            Student portal
          </button>
        </div>
  
        <!-- Navigation Links -->
        <nav class="flex-1 p-4 space-y-4">
          <router-link
            :to="`/students/${student_id}`"
            class="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white font-bold"
          >
            <i class="fas fa-graduation-cap mr-3"></i>
            Classes
          </router-link>
          <router-link
            :to="`/students/${student_id}/request`"
            class="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white font-bold"
          >
            <i class="fas fa-comments mr-3"></i>
            Requests
          </router-link>
        </nav>
  
        <!-- Footer Links -->
        <div class="p-4 space-y-4">
          <router-link
            :to="`/students/${student_id}/settings`"
            class="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white"
          >
            <i class="fas fa-cog mr-3"></i>
            Settings
          </router-link>
          <router-link
            :to="`/students/${student_id}/profile`"
            class="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white"
          >
            <i class="fas fa-user mr-3"></i>
            Profile
          </router-link>
        </div>
      </aside>
  
      <!-- Main Content -->
      <main class="flex-1 bg-gray-50 p-6">
        <router-view></router-view>
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const student_id = ref(); // The ID of the student for routes
  
  onMounted(() => {
    student_id.value = route.params.studentId as string;
  });
  </script>
  
  <style scoped>
  aside a {
    transition: color 0.3s ease, background-color 0.3s ease;
  }
  aside a.active {
    background-color: #000000; /* Active background */
    color: #ffffff; /* Active text color */
  }
  </style>
  