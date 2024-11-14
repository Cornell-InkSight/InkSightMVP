<template>
<ProfessorPortalNavbar />
<div class="p-6 max-w-6xl mx-auto bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-4">Courses</h1>

    <!-- Courses Grid -->
    <div v-if="!showRecordingPortal" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
    <div v-for="course in courses" :key="course.id" class="p-4 bg-white rounded-lg shadow-md border border-gray-200">
        <h2 class="text-lg font-semibold">{{ course.name }}</h2>
        <p class="text-sm text-gray-600">{{ course.description }}</p>
        
        <!-- Start Recording Button -->
        <button 
        @click="startRecording(String(course.id))" 
        class="mt-4 bg-blue-500 text-white py-2 px-4 rounded-full hover:bg-blue-600"
        >
        Record Lecture
        </button>
    </div>
    </div>

    <!-- Recording Portal -->
    <RecordingPortal 
    v-if="showRecordingPortal" 
    :courseId="selectedcourseId" 
    @closePortal="closeRecordingPortal" 
    />
</div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import RecordingPortal from '@/components/ProfessorPortal/ProfessorRecordingPortal.vue';
  import { fetchCoursesForProfessors } from '@/services/api/fetch';
  import { useRoute } from 'vue-router';
  import * as interfaces from "@/services/api/interfaces";
  import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue"

  const courses = ref<interfaces.Course[]>([]);
  const showRecordingPortal = ref(false);
  const selectedcourseId = ref<string>("");
  
  const route = useRoute();
  const professorId = route.params.professorId as string;
  
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
  
  onMounted(async () => {
      await loadCoursesForProfessor(professorId);
  });
  </script>
  