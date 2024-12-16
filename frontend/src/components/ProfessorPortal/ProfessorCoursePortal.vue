<template>
<div class="flex min-h-screen bg-gray-100">
    <ProfessorPortalNavbar />
    <div class="p-6 bg-gray-100 min-h-screen w-[80%]">
      <!-- Main Content -->
      <main class="flex-1 bg-gray-50 px-8 py-6" v-if="!showRecordingPortal">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-3xl font-bold">Courses</h1>
          <div>
            <!-- Search and View Options -->
            <input
              type="text"
              placeholder="Search"
              class="border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button class="ml-4 p-2 bg-black text-white rounded hover:bg-gray-800">
              <span class="sr-only">Switch view</span>
              ⬛
            </button>
          </div>
        </div>
  
        <!-- Course Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="course in courses"
            :key="course.id"
            class="bg-white border border-gray-200 rounded-lg shadow-sm p-6"
          >
            <h2 class="text-xl font-bold text-gray-900 mb-2 w-[100%]">{{ course.name.split(": ")[0] }}</h2>
            <p class="text-sm text-gray-600">{{ course.name.split(": ")[1] }}</p>
            <div class="mt-4 flex space-x-4">
              <button
                class="flex items-center justify-center border border-gray-300 rounded-lg px-4 py-2 text-gray-700 hover:bg-gray-100"
                @click="startRecording(String(course.id))"
              >
                🎥 Record lecture
              </button>
              <button
                class="flex items-center justify-center border border-gray-300 rounded-lg px-4 py-2 text-gray-700 hover:bg-gray-100"
              >
                ⬆️ Upload lecture
              </button>
            </div>
          </div>
        </div>
      </main>
      <!-- Recording Portal -->
      <RecordingPortal 
        v-if="showRecordingPortal" 
        :courseId="selectedcourseId" 
        @closePortal="closeRecordingPortal" 
       />
    </div>
</div>
</template>
  

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import RecordingPortal from '@/components/ProfessorPortal/ProfessorRecordingPortal.vue';
import { fetchCoursesForProfessors } from '@/services/api/fetch';
import { useRoute } from 'vue-router';
import * as interfaces from "@/services/api/interfaces";
import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue"
import { useUserStore } from "@/stores/authStore"

const courses = ref<interfaces.Course[]>([]);
const showRecordingPortal = ref(false);
const selectedcourseId = ref<string>("");

const route = useRoute();

/**
 * Fetches the courses for a specific professor
 */
const loadCoursesForProfessor = async (professorId: string) => {
    const { data, error } = await fetchCoursesForProfessors(professorId);
    if (error) {
        console.error(error);
        return;
    }
    courses.value = data;
};

/**
 * Opens the recording portal for the selected course.
 * @param {string} courseId - The name of the course to display in the recording portal.
 */
const startRecording = (courseId: string) => {
    selectedcourseId.value = courseId;
    showRecordingPortal.value = true;
};

/**
 * Closes the recording portal and returns to the course list.
 */
const closeRecordingPortal = () => {
    showRecordingPortal.value = false;
    selectedcourseId.value = "";
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
    const userStore = useUserStore()
    await userStore.fetchUser()
    const user = userStore.user;
    const professorId = user.user_ptr_id;
    await loadCoursesForProfessor(professorId);
});
</script>
  