<template>
  <StudentPortalNavbar />
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
        <div v-if="course.professors && course.professors.length > 0" class="mt-2">
                <h4 class="text-sm font-semibold text-gray-700">Professors:</h4>
                <ul class="mt-1 space-y-1">
                    <li
                    v-for="professor in course.professors"
                    :key="professor.id"
                    class="text-sm text-gray-600 bg-gray-100 rounded-md p-2"
                    >
                    {{ professor.name }}
                    </li>
                </ul>
            </div>
        <p class="mt-2 text-sm text-gray-500">{{ course.instructor }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { fetchStudent, fetchCourses, fetchProfessorsForCourses, fetchNotetakingRequestsForCourses } from "@/services/api/fetch"
import * as interfaces from "@/services/api/interfaces"
import StudentPortalNavbar from '@/components/StudentPortal/StudentPortalNavbar.vue'

const route = useRoute()
const courses = ref<any[]>([]) // Holds data for students courses, initially empty
const student = ref(null) // Holds data for student, initially null
const loading = ref<boolean>(true) // Loading state indicator
const error = ref<string | null>(null) // Error message, if any

/**
 * Fetches data for the given student and assigns it to `student`
 * Logs error message if request fails
 * 
 * @param studentId // The id of the given student, from route params
 * @returns {Promise<Void>} // A Promise that resolves when the data is fetched and assigned
 */
const loadStudent = async (studentId: string) => {
  const { data, error: studentError } = await fetchStudent(studentId);
  if (studentError) {
    error.value = studentError;
    return;
  } 
  student.value = data;
};

/**
 * Fetches data for the courses for the given student and assigns it to `courses`
 * Logs error message if request fails. Also fetches the professor for each course.
 * @param studentId // the id of the given student, from route params
 * @returns {Promise<Void>} // A Promise that resolves when the data is fetched and assigned
 */
const loadCourses = async (studentId: string) => {
  const { data, error: coursesError } = await fetchCourses(studentId);
  if (coursesError) {
    error.value = coursesError;
  } else {
    const coursePromises = data.map(async (course: interfaces.Course) => {
      const professors = await loadProfessorsForCourses(course.id);
      
      return {
        ...course,
        professors
      }
    })
    courses.value = await Promise.all(coursePromises); 
  }
};

/**
 * Fetches the Professors Data for the given course id, used in loop
 * Logs error, if the request fails
 */
 const loadProfessorsForCourses = async (courseId: string) => {
    const { data, error } = await fetchProfessorsForCourses(courseId);
    if(error) {
        console.error(error);
        return;
    }
    return data;
}

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
  const studentId = route.params.studentId as string
  await loadStudent(studentId);
  await loadCourses(studentId);
  loading.value = false; 
})
</script>
