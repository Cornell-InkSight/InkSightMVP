<template>
  <div class="max-w-6xl mx-auto p-6 bg-gray-100 min-h-screen">
    <!-- Header with Title and Layout Options -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-gray-900">
        Classes for <span v-if="student">{{ student.name }}</span>
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
        v-for="course in courses" 
        :key="course.id" 
        class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
      >
        <h2 class="text-xl font-bold text-gray-800">{{ course.name }}</h2>
        <p class="text-gray-600">{{ course.description }}</p>
        <p class="mt-2 text-sm text-gray-500">{{ course.instructor }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const courses = ref<any[]>([])
const student = ref(null)
const loading = ref<boolean>(true)
const error = ref<string | null>(null)

const fetchStudent = async (studentId: string) => {  
  try {
    const response = await axios.get(`http://127.0.0.1:8000/usermanagement/students/${studentId}`)
    student.value = response.data;
  } catch (err) {
    error.value = "Failed to load student"
  }
}

const fetchCourses = async (studentId: string) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/coursemanagement/students/${studentId}/courses/`)
    console.log("Courses data:", JSON.stringify(response.data, null, 2))  
    courses.value = response.data
  } catch (err) {
    error.value = "Failed to load courses"
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const studentId = route.params.studentId as string
  await fetchStudent(studentId)
  await fetchCourses(studentId)
})
</script>
