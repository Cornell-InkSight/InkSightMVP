<template>
  <ProfessorPortalNavbar />
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
          v-for="(students, courseId) in students" 
          :key="courseId" 
          class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
      >
        <!-- Course Header -->
        <h2 class="text-xl font-bold text-gray-800">{{ courseNames[courseId] || "Loading..." }}</h2>

        <!-- List of Students for Each Course -->
        <ul class="mt-2 space-y-1">
          <li 
              v-for="student in students" 
              :key="student.id" 
              :class="{'bg-yellow-100 border-l-4 border-yellow-500': hasActiveNoteTakingRequest(student.id)}"
              class="text-sm text-gray-600 rounded-md p-2"
          >
            <p class="font-semibold">{{ student.name }}</p>
            <p class="text-xs">{{ student.disability }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { fetchStudentsForProfessors, fetchProfessor, fetchNotetakingRequestsForCourses, fetchCourse } from '@/services/api/fetch';
import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue";

const route = useRoute();
const professor = ref<any | null>(null);  // Holds professor data, initially null
const students = ref<any[]>([]);   // Holds list of courses+students associated with professor
const loading = ref<boolean>(true);       // Loading state indicator
const error = ref<string | null>(null);   // Error message, if any
const noteTakingRequests = ref<Record<string, boolean>>({}); // Tracks active note-taking requests by student ID
const courseNames = ref<Record<string, string>>({});  // Dictionary to store course names by ID

/**
 * Fetches students and courses for a specific professor by ID and assigns them to `studentscourses`.
 * Logs an error message if the request fails.
 *
 * @param {string} professorId - The ID of the professor whose courses+students are being fetched.
 * @returns {Promise<void>} - A Promise that resolves when the data is fetched and assigned.
 */
const loadStudents = async (professorId: string): Promise<void> => {
  const { data, error: fetchError } = await fetchStudentsForProfessors(professorId);
  if (fetchError) {
    console.error(fetchError);
    error.value = fetchError;
    return;
  }
  students.value = data;
  await loadCourseNames();
}

/**
 * Fetches data for a specific professor by ID and assigns it to `professor`.
 * Logs an error message if the request fails.
 *
 * @param {string} professorId - The ID of the professor to fetch.
 * @returns {Promise<void>} - A Promise that resolves when the data is fetched and assigned.
 */
const loadProfessor = async (professorId: string): Promise<void> => {
  const { data, error: fetchError } = await fetchProfessor(professorId);
  if (fetchError) {
    console.error(fetchError);
    error.value = fetchError;
    return;
  }
  professor.value = data;
}

/**
 * Loads course names for each course ID in `studentscourses`.
 */
const loadCourseNames = async (): Promise<void> => {
  for (const courseId of Object.keys(students.value)) {
    const { data, error: fetchError } = await fetchCourse(courseId);
    if (!fetchError && data) {
      courseNames.value[courseId] = data.name;
    } else {
      console.error(`Failed to fetch course name for course ID ${courseId}:`, fetchError);
    }
  }
}


/**
 * Loads note-taking requests for each course and populates `noteTakingRequests`.
 */
 const loadStudentCourses = async (): Promise<void> => {
  for (const courseId of Object.keys(students.value)) {
    const { data, error: fetchError } = await fetchNotetakingRequestsForCourses(courseId);
    if (!fetchError && data) {
      data.forEach((request: any) => {
        noteTakingRequests.value[request.student_id] = true;
      });
    } else {
      console.error(`Failed to fetch note-taking requests for course ID ${courseId}:`, fetchError);
    }
  }
}

/**
 * Checks if a student has an active note-taking request.
 *
 * @param {string} studentId - The ID of the student to check.
 * @returns {boolean} - Returns true if the student has an active request, false otherwise.
 */
const hasActiveNoteTakingRequest = (studentId: string): boolean => {
  return !!noteTakingRequests.value[studentId];
}

/**
 * Watch noteTakingRequests to update highlighting
 */
watch(noteTakingRequests, () => {

})

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
  const professorId = route.params.professorId as string;
  await loadProfessor(professorId);
  await loadStudents(professorId);
  await loadStudentCourses()
  loading.value = false;
});
</script>

<style scoped>
/* Additional styles for highlighting */
.bg-yellow-100 {
  background-color: #fef3c7;
}
.border-l-4 {
  border-left-width: 4px;
}
.border-yellow-500 {
  border-color: #d97706;
}
</style>
