<template>
<nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex items-center justify-between">
        <!-- Logo or Title -->
        <h1 class="text-white text-2xl font-bold">SDS Portal</h1>
o
        <!-- Navigation Links -->
        <div class="flex space-x-4">
            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white"> 
                <router-link
                :to="`/sdscoordinators/${sds_coordinator_id}`"
                >
                Students
                </router-link>
            </div>
            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white">
                <router-link
                :to="`/sdscoordinators/${sds_coordinator_id}/courses`"
                >
                Courses
                </router-link>
            </div> 

            <div class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium" active-class="text-white">
                <router-link
                :to="`/sdscoordinators/${sds_coordinator_id}/professors`"
                >
                Professors
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
const sds_coordinator_id = ref(); // the id of the SDS Coordinator for routes

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for SDS Coordinator ID.
 */
onMounted(() => {
    sds_coordinator_id.value = route.params.sdscoordinatorId as string
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
