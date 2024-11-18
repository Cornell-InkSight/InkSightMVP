<template>
  <StudentPortalNavbar />
  <div class="max-w-6xl mx-auto p-6 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-gray-900">
        Classes for <span v-if="student">{{ student.name }}</span>
      </h1>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="text-center text-gray-500">
      <span class="animate-pulse">Loading courses...</span>
    </div>
    <div v-else-if="error" class="text-center text-red-500 font-semibold">
      {{ error }}
    </div>

    <!-- Course List -->
    <div v-else class="space-y-4">
      <div 
        v-for="course in courses" 
        :key="course.id" 
        class="bg-white rounded-lg shadow-md border border-gray-200"
      >
        <!-- Course Header -->
        <div 
          @click="toggleCourseDetails(course.id)" 
          class="p-4 flex justify-between items-center cursor-pointer"
        >
          <h2 class="text-xl font-bold text-gray-800">{{ course.name }}</h2>
          <i 
            :class="{
              'fas fa-chevron-down': !expandedCourses.includes(course.id),
              'fas fa-chevron-up': expandedCourses.includes(course.id)
            }"
            class="text-gray-500"
          ></i>
        </div>

        <!-- Expanded Details -->
        <div v-if="expandedCourses.includes(course.id)" class="p-4 border-t border-gray-300">
          <!-- Ongoing Lecture Alert -->
          <div v-if="course.ongoingLectureSession" class="flex items-center text-blue-600 mb-2">
            <i class="fas fa-broadcast-tower text-lg mr-2"></i>
            <span>Ongoing Lecture Session</span>
          </div>

          <!-- Professors Section -->
          <div v-if="course.professors && course.professors.length > 0" class="mb-4">
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

          <!-- Approval Check -->
          <div v-if="course.isApprovedForCourse">
            <!-- Notes Packets -->
            <div v-if="course.notesPackets && course.notesPackets.length > 0" class="mb-4">
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
          <div v-else class="text-sm text-red-500">
            You are not approved for this course. Please request access in the Requests tab.
          </div>
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
const expandedCourses = ref<number[]>([]); 

/**
 * Loads the data for the student from the API
 * @param studentId - ID of the student
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
 * Loads the courses for respective student, returns dictionary object with extra info needed for each course
 * Sets up Professors, top 5 most recent Notes Packets, and checks if student is approved for course by calling helper functions
 * Checks if theirs an ongoing lecture 
 * @param studentId - the ID of the student
 */
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

/**
 * Loads the professors for the course
 * @param courseId - ID of the course
 */
const loadProfessorsForCourses = async (courseId: string) => {
  const { data, error } = await fetchProfessorsForCourses(courseId);
  if (error) {
    console.error(error);
    return;
  }
  return data;
};

/**
 * Loads the published note packets for the course
 * @param courseId - ID of the course
 */
const loadNotesPacketsForCourse = async (courseId: number) => {
  const { data, error } = await fetchPublishedNotePacketsForCourse(courseId);
  if (error) {
    console.error(error);
    return [];
  }
  return data;
};

/**
 * Loads whether the student is approved for the respective course by the professor(s)
 * @param studentId - the ID of the student
 * @param courseId - the ID of the course
 */
const loadIsStudentApprovedForCourse = async (studentId: string, courseId: string) => {
  const { data, error } = await fetchIsApprovedStudentForCourse(studentId, courseId);
  if (error) {
    console.error(error);
    return false;
  }
  return data;
};

/**
 * Toggles course details visibility
 * @param courseId - ID of the course to toggle
 */
 const toggleCourseDetails = (courseId: number) => {
  if (expandedCourses.value.includes(courseId)) {
    expandedCourses.value = expandedCourses.value.filter(id => id !== courseId);
  } else {
    expandedCourses.value.push(courseId);
  }
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for the student and their courses and additional data.
 */
onMounted(async () => {
  const studentId = route.params.studentId as string;
  await loadStudent(studentId);
  await loadCourses(studentId);
  loading.value = false; 
});
</script>
