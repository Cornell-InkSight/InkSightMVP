<template>
<nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex items-center justify-between">
        <!-- Logo or Title -->
        <h1 class="text-white text-2xl font-bold">Student Portal</h1>
o
        <!-- Navigation Links -->
        <div class="flex space-x-4">
            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white"> 
                <router-link
                :to="`/students/${student_id}`"
                >
                Home
                </router-link>
            </div>
            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white">
                <router-link
                :to="`/students/${student_id}/request`"
                >
                Requests
                </router-link>
            </div> 
        </div>
    </div>
</nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const student_id = ref();

onMounted(() => {
    student_id.value = route.params.studentId as string
})
</script>

<style scoped>
nav {
background-color: #1f2937;
}

nav a {
transition: color 0.3s ease;
}
</style>
