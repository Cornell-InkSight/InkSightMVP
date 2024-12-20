<template>
  <div class="flex min-h-screen bg-gray-100">
    <ProfessorPortalNavbar class="sticky"/>
    <div class="p-6 bg-gray-100 min-h-screen w-[80%]">
      <div v-if="!showRecordingPortal">
        <!-- Header with Title and Layout Options -->
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-3xl font-bold text-gray-900">
            <span v-if="professor">{{ professor.name }}</span>
          </h1>
          <div class="flex items-center space-x-4">
            <!-- Search Bar -->
            <input 
              type="text" 
              placeholder="Search" 
              class="px-4 py-2 border border-gray-300 rounded-md focus:ring focus:border-blue-300"
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
        

        <!-- Course Details Modal -->
        <transition name="fade" mode="out-in">
          
            <ProfessorCourseView 
              v-if="selectedProfessorCourseStore.selectedCourse" 
              @closeModal="selectedProfessorCourseStore.selectedCourse = null"
            />
            
         <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="(students, courseId) in students" 
            :key="courseId" 
            class="p-4 bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col justify-between items-stretch"
          >
            <!-- Course Header -->
            <div>
              <div class="flex">
                <h2 class="text-xl font-bold text-gray-900 mb-2 w-[100%]">{{ courses[courseId].name.split(": ")[0] }}</h2>
                <button class="text-gray-500 hover:text-gray-700" @click="selectedProfessorCourseStore.setCourse(courses[courseId])">
                  <!-- Vertical Ellipsis Icon -->
                  <i class="fas fa-info-circle"></i>
                </button>
              </div>
              <p class="text-sm text-gray-600">{{ courses[courseId].name.split(": ")[1] }}</p>
            </div>
            
    
            <!--Recording-->
            <div class="mb-4">
              <div class="mt-4 flex space-x-4">
                <button
                  class="flex items-center justify-center border border-gray-300 rounded-lg px-4 py-2 text-gray-700 hover:bg-gray-100"
                  @click="startRecording(courses[courseId])"
                >
                  <i class="fas fa-camera mr-2"></i> Record
                </button>
                <button
                  class="flex items-center justify-center border border-gray-300 rounded-lg px-4 py-2 text-gray-700 hover:bg-gray-100"
                >
                <i class="fas fa-upload mr-2"></i> Upload
                </button>
              </div>
            </div>
          </div>
        </div>
        </transition>
      </div> 
      <!-- Recording Portal -->
      <RecordingPortal 
      v-if="showRecordingPortal" 
      :courseId="selectedCourse.id" 
      @closePortal="closeRecordingPortal" 
      />
    </div>
  </div>  
</template>
  
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { fetchStudentsForProfessors, fetchProfessor, fetchNotetakingRequestsForCourses, fetchCourse, fetchStudentCourses, fetchNoteTakingRequestStudentForCourse, fetchCoursesForProfessors } from '@/services/api/fetch';
import * as interfaces from "@/services/api/interfaces"
import { approveNoteTakingRequest } from "@/services/api/add";
import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue"
import { useUserStore } from "@/stores/authStore";
import Swal from 'sweetalert2';
import RecordingPortal from '@/components/ProfessorPortal/ProfessorRecordingPortal.vue';
import ProfessorCourseView from '@/components/ProfessorPortal/ProfessorCourseView.vue'
import { useSelectedProfessorCourseStore } from "@/stores/selectedProfessorCourseStore"
import { icon } from '@fortawesome/fontawesome-svg-core';


const route = useRoute();
const professor = ref<any | null>(null);  // Holds professor data, initially null
const students = ref<any[]>([]);          // Holds list of courses+students associated with professor
const loading = ref<boolean>(true);       // Loading state indicator
const error = ref<string | null>(null);   // Error message, if any
const noteTakingRequests = ref<Record<string, { approved: boolean; requestId: string }>>({}); // Tracks note-taking requests by `studentId-courseId` key with approval status
const courses = ref<Record<string, interfaces.Course>>({});         // Dictionary to store course names by ID
const openDropdownId = ref<string | null>(null);    // Tracks open dropdown for each student

const showRecordingPortal = ref(false);
const selectedCourse = ref<interfaces.Course>(); // The course selected for the modal and recording
const selectedProfessorCourseStore = useSelectedProfessorCourseStore();

// Store tooltip content to avoid async issues
const tooltipContentCache = ref<Record<string, string>>({});

/**
 * Fetches students and courses for a specific professor by ID and assigns them to `studentscourses`.
 */
const loadStudents = async (professorId: string): Promise<void> => {
  const { data, error: fetchError } = await fetchStudentsForProfessors(professorId);
  if (fetchError) {
    console.error(fetchError);
    error.value = fetchError;
    return;
  }
  students.value = data;
  await loadCourses();
};

/**
 * Fetches data for a specific professor by ID and assigns it to `professor`.
 */
const loadProfessor = async (professorId: string): Promise<void> => {
  const { data, error: fetchError } = await fetchProfessor(professorId);
  if (fetchError) {
    console.error(fetchError);
    error.value = fetchError;
    return;
  }
  professor.value = data;
};

/**
 * Loads course names for each course ID in `studentscourses`.
 */
const loadCourses = async (): Promise<void> => {
  for (const courseId of Object.keys(students.value)) {
    const { data, error: fetchError } = await fetchCourse(courseId);
    if (!fetchError && data) {
      courses.value[courseId] = data;
    } else {
      console.error(`Failed to fetch course name for course ID ${courseId}:`, fetchError);
    }
  }
};

/**
 * Loads note-taking requests for each course and populates `noteTakingRequests`.
 */
const loadNoteTakingRequestsForCourses = async () => {
  for (const courseId of Object.keys(courses.value)) {
    const { data, error: requestsError } = await fetchNotetakingRequestsForCourses(courseId);
    if (requestsError) {
      console.error(requestsError);
      error.value = requestsError;
    } else {
      for (const request of data) {
        const studentCourse = await fetchStudentCourses(request.student_course_id);
        const key = `${studentCourse.data.student_id}-${studentCourse.data.course_id}`;
        noteTakingRequests.value[key] = { approved: request.approved, requestId: request.id };
      }
    }
  }
};

/**
 * Returns a tooltip message for a student's note-taking request.
 */
const tooltipContent = (studentId: string, courseId: string) => {
  const key = `${studentId}-${courseId}`;

  // If already cached, return it
  if (tooltipContentCache.value[key]) return tooltipContentCache.value[key];

  // Otherwise, load and cache
  loadNoteTakingRequestStudentForCourse(studentId, courseId).then(data => {
    tooltipContentCache.value[key] = data?.request
      ? isApprovedNoteTakingRequest(studentId, courseId)
        ? `Approved request: ${data.request}`
        : `Click to approve: ${data.request}`
      : "No request data available. Please notify student to send request.";
  });

  // Return a loading message until resolved
  return "Loading request data...";
};

/**
 * Checks if a note-taking request for a specific student and course is approved.
 */
const isApprovedNoteTakingRequest = (studentId: string, courseId: string): boolean => {
  const key = `${studentId}-${courseId}`;
  return noteTakingRequests.value[key]?.approved || false;
};

/**
 * Fetches the Student Course Notetaking Request
 */
const loadNoteTakingRequestStudentForCourse = async (studentId: string, courseId: string) => {
  const { data, error: fetchError } = await fetchNoteTakingRequestStudentForCourse(studentId, courseId);
  if (fetchError) {
    console.error(fetchError);
    error.value = fetchError;
    return null;
  }
  return data;
};


/**
 * Opens the recording portal for the selected course.
 * @param {string} courseId - The name of the course to display in the recording portal.
 */
const startRecording = (courseId: interfaces.Course) => {
  
  selectedCourse.value = courseId;
  showRecordingPortal.value = true;
};

/**
 * Closes the recording portal and returns to the course list.
 */
const closeRecordingPortal = () => {
    showRecordingPortal.value = false;
    selectedCourse.value = null;
};


/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
  // Load User Data
  const userStore = useUserStore()
  await userStore.fetchUser()
  const user = userStore.user;
  const professorId = user.user_ptr_id;
  await loadProfessor(professorId);
  await loadStudents(professorId);
  await loadNoteTakingRequestsForCourses(); 
  // Selected Course for Reactive Navbar
  selectedCourse.value = selectedProfessorCourseStore.selectedCourse;
  loading.value = false;      
});
</script>


<style scoped>
/* Additional styles for highlighting */
.bg-yellow-100 {
  background-color: #fef3c7;
}
.border-yellow-500 {
  border-color: #d97706;
}
.bg-green-100 {
  background-color: #d1fae5;
}
.border-green-500 {
  border-color: #10b981;
}

.tippy-box[data-theme~='light-border'] {
  border: 1px solid #e5e7eb;
  background-color: #ffffff;
  color: #4b5563;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.tippy-box[data-theme~='light-border'] .tippy-content {
  font-size: 0.875rem; /* Small font for readability */
  line-height: 1.25;
}

.tippy-box[data-theme~='light-border'] .tippy-arrow {
  color: #ffffff;
}
</style>