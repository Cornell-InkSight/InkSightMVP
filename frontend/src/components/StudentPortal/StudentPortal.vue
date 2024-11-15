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

        <!-- Ongoing Lecture Alert -->
        <div v-if="course.ongoingLectureSession" class="flex items-center text-blue-600 mt-2">
          <i class="fas fa-broadcast-tower text-lg mr-2"></i>
          <span>Ongoing Lecture Session</span>
        </div>

        <!-- Professors Section -->
        <div v-if="course.professors && course.professors.length > 0" class="mt-2">
          <h4 class="text-sm font-semibold text-gray-700">Professors:</h4>
          <ul class="mt-1 space-y-1">
            <li v-for="professor in course.professors" :key="professor.id" class="text-sm text-gray-600 bg-gray-100 rounded-md p-2">
              {{ professor.name }}
            </li>
          </ul>
        </div>

        <!-- Approval Check -->
        <div v-if="course.isApprovedForCourse">
          <!-- Most Recent Notes Packets -->
          <div v-if="course.notesPackets && course.notesPackets.length > 0" class="mt-4">
            <h4 class="text-sm font-semibold text-gray-700">Recent Notes Packets:</h4>
            <ul class="mt-1 space-y-1">
              <li 
                v-for="packet in course.notesPackets" 
                :key="packet.id" 
                class="text-sm text-gray-500 bg-gray-50 rounded-md p-2 hover:bg-gray-100"
              >
                <div class="text-blue-500 hover:underline">
                  <router-link :to="`/notepackets/${packet.id}/`" target='_blank'>
                    Packet from Lecture Session {{ packet.lecture_session_id }}
                  </router-link>
                </div>
              </li>
            </ul>
          </div>
          <p v-else class="text-sm text-gray-500">No recent notes packets available.</p>
        </div>

        <!-- Not Approved Message -->
        <div v-else class="text-sm text-red-500 mt-4">
          You are not approved for this course. Please request access in the Requests tab.
        </div>
      </div>
    </div>
  </div>  
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { 
  fetchStudent, 
  fetchCourses, 
  fetchProfessorsForCourses, 
  fetchPublishedNotePacketsForCourse, 
  fetchIsApprovedStudentForCourse,
  fetchCurrentOngoingLectureSession
} from "@/services/api/fetch";
import * as interfaces from "@/services/api/interfaces";
import StudentPortalNavbar from '@/components/StudentPortal/StudentPortalNavbar.vue';

const route = useRoute();
const courses = ref<any[]>([]);
const student = ref(null);
const loading = ref<boolean>(true);
const error = ref<string | null>(null);

const loadStudent = async (studentId: string) => {
  const { data, error: studentError } = await fetchStudent(studentId);
  if (studentError) {
    error.value = studentError;
    return;
  } 
  student.value = data;
};

const loadCourses = async (studentId: string) => {
  const { data, error: coursesError } = await fetchCourses(studentId);
  if (coursesError) {
    error.value = coursesError;
  } else {
    const coursePromises = data.map(async (course: interfaces.Course) => {
      const professors = await loadProfessorsForCourses(course.id);
      const notesPackets = await loadNotesPacketsForCourse(course.id);
      const isApprovedForCourse = await loadIsStudentApprovedForCourse(studentId, course.id);

      const { data: ongoingLectureData, error: ongoingLectureError } = await fetchCurrentOngoingLectureSession(course.id);
      const ongoingLectureSession = !ongoingLectureError && ongoingLectureData;

      
      const recentNotesPackets = notesPackets.slice(0, 5).reverse();  

      return {
        ...course,
        professors,
        notesPackets: recentNotesPackets,
        isApprovedForCourse,
        ongoingLectureSession,
      };
    });
    courses.value = await Promise.all(coursePromises); 
  }
};

const loadProfessorsForCourses = async (courseId: string) => {
  const { data, error } = await fetchProfessorsForCourses(courseId);
  if (error) {
    console.error(error);
    return;
  }
  return data;
};

const loadNotesPacketsForCourse = async (courseId: number) => {
  const { data, error } = await fetchPublishedNotePacketsForCourse(courseId);
  if (error) {
    console.error(error);
    return [];
  }
  return data;
};

const loadIsStudentApprovedForCourse = async (studentId: string, courseId: string) => {
  const { data, error } = await fetchIsApprovedStudentForCourse(studentId, courseId);
  if (error) {
    console.error(error);
    return false;
  }
  return data;
};

onMounted(async () => {
  const studentId = route.params.studentId as string;
  await loadStudent(studentId);
  await loadCourses(studentId);
  loading.value = false; 
});
</script>
