<template>
<nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex items-center justify-between">
        <!-- Logo or Title -->
        <h1 class="text-white text-2xl font-bold">Professor Portal</h1>
o
        <!-- Navigation Links -->
        <div class="flex space-x-4">
            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white"> 
                <router-link
                :to="`/professors`"
                >
                Students
                </router-link>
            </div>
            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white">
                <router-link
                :to="`/professors/courses`"
                >
                Courses
                </router-link>
            </div> 

            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white">
                <router-link
                :to="`/professors/lectures`"
                >
                Publish Notes Packets
                </router-link>
            </div>
        </div>
    </div>
</nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from "@/stores/authStore"

const route = useRoute()
const professor_id = ref();

// onMounted(async () => {
//     const userStore = useUserStore()
//     await userStore.fetchUser()
//     const user = userStore.user;
//     professor_id.value = user.user_ptr_id as string
// })
</script>

<style scoped>
nav {
background-color: #1f2937;
}

nav a {
transition: color 0.3s ease;
}
</style>
