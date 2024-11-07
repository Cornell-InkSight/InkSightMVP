<template>
<div class="max-w-6xl mx-auto p-6 bg-gray-100 min-h-screen">
    <!-- Header with Title and Layout Options -->
    <div class="flex items-center justify-between mb-6">
    <h1 class="text-3xl font-bold text-gray-900">
        Students of <span v-if="professor">{{ professor.name }}</span>
    </h1>
    <div class="flex items-center space-x-4">
        <!-- Search Bar -->
        <input 
        type="text" 
        placeholder="Search" 
        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300"
        />
        <!-- Layout Icons -->
        <button class="p-2 rounded-md hover:bg-gray-200">
        <i class="fas fa-th-list"></i> <!-- List icon -->
        </button>
        <button class="p-2 rounded-md hover:bg-gray-200">
        <i class="fas fa-th"></i> <!-- Grid icon -->
        </button>
    </div>
    </div>

    <!-- Course Grid -->
    <div v-if="loading" class="text-center text-gray-500">
    <span class="animate-pulse">Loading courses...</span>
    </div>
    <div v-else-if="error" class="text-center text-red-500 font-semibold">
    {{ error }}
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div 
        v-for="student in students" 
        :key="student.id" 
        class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
    >
        <h2 class="text-xl font-bold text-gray-800">{{ student.name }}</h2>
        <p class="text-gray-600">{{ student.description }}</p>
        <p class="mt-2 text-sm text-gray-500">{{ student.instructor }}</p>
    </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchStudentsForProfessors, fetchProfessor } from '@/services/api/fetch'

const route = useRoute()
const professor = ref<any | null>(null)  // Holds professor data, initially null
const students = ref<any[]>([])          // Holds list of students associated with professor
const loading = ref<boolean>(true)       // Loading state indicator
const error = ref<string | null>(null)   // Error message, if any

/**
 * Fetches students for a specific professor by ID and assigns them to `students`.
 * Logs an error message if the request fails.
 *
 * @param {string} professorId - The ID of the professor whose students are being fetched.
 * @returns {Promise<void>} - A Promise that resolves when the data is fetched and assigned.
 */
const loadStudents = async (professorId: string): Promise<void> => {
  const { data, error: fetchError } = await fetchStudentsForProfessors(professorId)
  if (fetchError) {
    console.error(fetchError)
    error.value = fetchError
    return
  }
  students.value = data
  console.log("Students:", data)
}

/**
 * Fetches data for a specific professor by ID and assigns it to `professor`.
 * Logs an error message if the request fails.
 *
 * @param {string} professorId - The ID of the professor to fetch.
 * @returns {Promise<void>} - A Promise that resolves when the data is fetched and assigned.
 */
const loadProfessor = async (professorId: string): Promise<void> => {
  const { data, error: fetchError } = await fetchProfessor(professorId)
  if (fetchError) {
    console.error(fetchError)
    error.value = fetchError
    return
  }
  professor.value = data
  console.log("Professor:", data)
}

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
  const professorId = route.params.professorId as string
  await loadProfessor(professorId)
  await loadStudents(professorId)
  loading.value = false
})
</script>
