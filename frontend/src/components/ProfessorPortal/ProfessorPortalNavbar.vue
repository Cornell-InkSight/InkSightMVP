<template>
    <div class="flex h-screen w-[15%] border-r-2 border-gray-100">
        <!-- Sidebar -->
        <aside class="w-full bg-gray-100 shadow-md flex flex-col">
        <!-- Header -->
        <div class="p-4 border-b">
            <button class="bg-blue-500 text-white text-sm px-4 py-2 rounded-lg w-full font-semibold">
            Professor Portal
            </button>
        </div>
    
        <!-- Navigation Links -->
        <nav class="flex-1 p-4">
            <ul class="space-y-2">
            <!-- Students -->
            <li>
                <router-link
                :to="`/professors`"
                class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
                active-class="bg-black text-white font-bold"
                >
                <i class="fas fa-user-graduate mr-3 text-lg"></i>
                Students
                </router-link>
            </li>
    
            <!-- Courses -->
            <li>
                <router-link
                :to="`/professors/courses`"
                class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
                active-class="bg-black text-white font-bold"
                >
                <i class="fas fa-book-open mr-3 text-lg"></i>
                Courses
                </router-link>
            </li>
    
            <!-- Professors -->
            <li>
                <router-link
                :to="`/professors/lectures`"
                class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
                active-class="bg-black text-white font-bold"
                >
                <i class="fas fa-chalkboard-teacher mr-3 text-lg"></i>
                Notes
                </router-link>
            </li>
            </ul>
        </nav>
    
        <!-- Footer Links -->
        <div class="p-4 border-t">
            <ul class="space-y-2">
            <!-- Settings -->
            <li>
                <router-link
                :to="`/sdscoordinators/settings`"
                class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
                active-class="bg-black text-white"
                >
                <i class="fas fa-cog mr-3 text-lg"></i>
                Settings
                </router-link>
            </li>
    
            <!-- Profile -->
            <li>
                <router-link
                :to="`/sdscoordinators/profile`"
                class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
                active-class="bg-black text-white"
                >
                <i class="fas fa-user mr-3 text-lg"></i>
                Profile
                </router-link>
            </li>
            </ul>
        </div>
        </aside>
    </div>
    </template>
    
    <script setup lang="ts">
    import { ref } from 'vue';
    </script>
    
    <style scoped>
    /* Sidebar Link Transitions */
    aside a {
    transition: color 0.3s ease, background-color 0.3s ease;
    }
    
    aside a.active {
    background-color: #000; /* Active background */
    color: #fff; /* Active text color */
    }
    </style>
      