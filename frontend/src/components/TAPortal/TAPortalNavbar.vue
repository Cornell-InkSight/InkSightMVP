<template>
<div class="flex h-screen w-[15%] border-r-2 border-gray-100">
    <!-- Sidebar -->
    <aside class="w-full bg-gray-100 shadow-md flex flex-col">
    <!-- Header -->
    <div class="p-4 border-b">
        <button class="bg-blue-500 text-white text-sm px-4 py-2 rounded-lg w-full font-semibold">
        TA Portal
        </button>
    </div>

    <!-- Navigation Links -->
    <nav class="flex-1 p-4">
        <ul class="space-y-2">
        <!-- Classes -->
        <li>
            <router-link
            :to="`/tas`"
            class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white font-bold"
            >
            <i class="fas fa-pen-to-square mr-3 text-lg"></i>
            Note Packets
            </router-link>
        </li>
        <li>
            <router-link
            :to="`/tas/edits`"
            class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white font-bold"
            >
            <i class="fas fa-i-cursor mr-3 text-lg"></i>
            Edit History
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
            :to="`/settings`"
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
            :to="`/profile`"
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
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import * as interfaces from "@/services/api/interfaces";
import { useUserStore } from "@/stores/authStore"

const ta_id = ref();

// onMounted(async () => {
// const userStore = useUserStore()
// await userStore.fetchUser()
// const user = userStore.user;
// const studentId = user.user_ptr_id;});
// </script>

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
    