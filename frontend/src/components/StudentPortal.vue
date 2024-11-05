<template>
    <div>
      <h1>Student Courses</h1>
      <div v-if="loading">Loading courses...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>
        <ul>
          <li v-for="course in courses" :key="course.id">
            {{ course.name }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const courses = ref<any[]>([])
  const loading = ref<boolean>(true)
  const error = ref<string | null>(null)
  
  const fetchCourses = async (studentId: string) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/students/${studentId}/courses/`)
      courses.value = response.data
    } catch (err) {
      error.value = "Failed to load courses"
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    const studentId = route.params.studentId as string
    fetchCourses(studentId)
  })
  </script>
  