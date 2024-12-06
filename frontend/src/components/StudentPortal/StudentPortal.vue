<template>
  <div class="flex min-h-screen bg-gray-100">
  <StudentPortalNavbar />
  <div class="p-6 bg-gray-100 min-h-screen w-[80%]">
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

    
    <div v-else class="border p-4 rounded-lg bg-gray-50 w-full">
   
      <!-- Course Details Modal -->
      <transition name="fade" mode="out-in">
          <StudentCourseView 
            v-if="selectedCourse" 
            :course="selectedCourse" 
            @closeModal="selectedCourse = null"
          />
          
          <!-- Course List -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 border-black">
            <div 
              v-for="course in courses" 
              :key="course.id" 
              class="p-4 bg-white rounded-lg border border-black cursor-pointer hover:shadow-lg"
            >
              <!-- Course Header -->
              <div 
                @click="toggleCourseDetails(course)" 
                class="p-4 justify-between items-center cursor-pointer"
              >
                <h2 class="text-xl font-bold text-gray-900 mb-2 w-[100%]">{{ course.name.split(": ")[0] }}</h2>
                <p class="text-sm text-gray-600">{{ course.name.split(": ")[1] }}</p>
                <!-- <i 
                  class= 'fas fa-chevron-up text-gray-500'
                ></i> -->
              </div>

              <!-- Expanded Details -->
              <div class="p-4 border-t border-gray-300">
                <!-- Ongoing Lecture Alert -->
                <div v-if="course.ongoingLectureSession" class="flex items-center text-blue-600 mb-2">
                  <i class="fas fa-broadcast-tower text-lg mr-2"></i>
                  <span>Ongoing Lecture Session</span>
                </div>

                <!-- Professors Section -->
                <div v-if="course.professors && course.professors.length > 0" class="mb-4">
                  <ul class="mt-1 space-y-1">
                    <li 
                      v-for="professor in course.professors" 
                      :key="professor.id" 
                      class="text-sm text-gray-500 mt-2"
                    >
                      {{ professor.name }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
      </transition>
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
  fetchCurrentOngoingLectureSession,
  fetchStudentNotePacketsForCourse
} from "@/services/api/fetch";
import { useUserStore } from "@/stores/authStore"
import * as interfaces from "@/services/api/interfaces";
import StudentPortalNavbar from '@/components/StudentPortal/StudentPortalNavbar.vue';
import StudentCourseView from '@/components/StudentPortal/StudentCourseView.vue'

const courses = ref<any[]>([]); // Holds the courses for the student
const student = ref(null); // Holds the data for the student
const loading = ref<boolean>(true); // Holds the loading state
const error = ref<string | null>(null); // Holds the error, if any
const selectedCourse = ref<String>(); // Holds the selected course the student is viewing

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
      const notesPackets = await loadNotesPacketsForCourse(parseInt(course.id));
      const isApprovedForCourse = await loadIsStudentApprovedForCourse(studentId, course.id);
      const studentNotePackets = await loadStudentNotesPacketsForCourse(studentId, course.id);

      const { data: ongoingLectureData, error: ongoingLectureError } = await fetchCurrentOngoingLectureSession(course.id);
      const ongoingLectureSession = !ongoingLectureError && ongoingLectureData;
      
      return {
        ...course,
        professors,
        notesPackets: notesPackets.reverse(),
        isApprovedForCourse,
        ongoingLectureSession,
        studentNotePackets
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
  const { data, error } = await fetchPublishedNotePacketsForCourse(courseId.toString());
  if (error) {
    console.error(error);
    return [];
  }
  return data;
};

/**
 * Loads the published note packets for the course
 * @param courseId - ID of the course
 */
 const loadStudentNotesPacketsForCourse = async (studentId: string, courseId: string) => {
  const { data, error } = await fetchStudentNotePacketsForCourse(studentId, courseId);
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
 * Opens Course Modal For respective course
 * @param courseId - the ID of the course to open the modal for
 */
const toggleCourseDetails = async (courseId : string) => {
  selectedCourse.value = courseId;
}

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for the student and their courses and additional data.
 */
onMounted(async () => {
  const userStore = useUserStore()
  await userStore.fetchUser()
  const user = userStore.user;
  const studentId = user.user_ptr_id;
  await loadStudent(studentId);
  await loadCourses(studentId);
  loading.value = false; 
});
</script>
