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
        <h2 class="text-xl font-bold text-gray-800">{{ courses[courseId] || "Loading..." }}</h2>

        <!-- List of Students for Each Course -->
        <ul class="mt-2 space-y-1">
          <li 
            v-for="student in students" 
            :key="student.id" 
            :class="{
              'bg-green-100 border-l-4 border-green-500': isApprovedNoteTakingRequest(student.id, courseId.toString()),
              'bg-yellow-100 border-l-4 border-yellow-500': hasActiveNoteTakingRequest(student.id, courseId.toString()) && !isApprovedNoteTakingRequest(student.id, courseId.toString())
            }"
            class="text-sm text-gray-600 rounded-md p-2 flex items-center justify-between relative"
          >
            <div @click="toggleDropdown(student.id, courseId.toString())" class="cursor-pointer">
              <p class="font-semibold text-gray-800">{{ student.name }}</p>
              <p class="text-xs text-gray-500">{{ student.disability }}</p>
            </div>

            <!-- Dropdown with Request Details -->
            <div
              v-if="isDropdownOpen(student.id, courseId.toString())"
              class="absolute top-full left-0 mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-lg p-3 z-10 text-gray-700"
            >
              <p v-if="hasActiveNoteTakingRequest(student.id, courseId.toString())">
                <strong>Status:</strong>
                {{ isApprovedNoteTakingRequest(student.id, courseId.toString()) ? 'Approved' : 'Pending approval' }}
              </p>
              <p ><strong>Request Details:</strong> {{ getRequestTooltip(student.id, courseId.toString()) }}</p>
            </div>

            <div v-if="hasActiveNoteTakingRequest(student.id, courseId.toString()) && !isApprovedNoteTakingRequest(student.id, courseId.toString())">
              <!-- Approve Button -->
              <button 
                @click="approveRequest(student.id, courseId.toString())" 
                class="text-green-600 hover:text-green-800"
              >
                ✔️
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { fetchStudentsForProfessors, fetchProfessor, fetchNotetakingRequestsForCourses, fetchCourse, fetchStudentCourses, fetchNoteTakingRequestStudentForCourse } from '@/services/api/fetch';
import { approveNoteTakingRequest } from "@/services/api/add";
import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue";
import Swal from 'sweetalert2';

const route = useRoute();
const professor = ref<any | null>(null);  // Holds professor data, initially null
const students = ref<any[]>([]);          // Holds list of courses+students associated with professor
const loading = ref<boolean>(true);       // Loading state indicator
const error = ref<string | null>(null);   // Error message, if any
const noteTakingRequests = ref<Record<string, { approved: boolean; requestId: string }>>({}); // Tracks note-taking requests by `studentId-courseId` key with approval status
const courses = ref<Record<string, string>>({});         // Dictionary to store course names by ID
  const openDropdownId = ref<string | null>(null);    // Tracks open dropdown for each student

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
      courses.value[courseId] = data.name;
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
 * Gets request tooltip content for a specific student and course.
 */
 const getRequestTooltip = (studentId: string, courseId: string): string => {
  return tooltipContent(studentId, courseId);
};


/**
 * Approves a note-taking request.
 */
const approveRequest = async (studentId: string, courseId: string) => {
  const key = `${studentId}-${courseId}`;
  const request = noteTakingRequests.value[key];
  
  if (request && !request.approved) {
    const { data, error } = await approveNoteTakingRequest(request.requestId);
    if (error) {
      console.error("Failed to approve request:", error);
      return;
    }
    Swal.fire({
      title: 'Request Approved',
      text: `The request has been approved.`,
      icon: 'success',
      confirmButtonText: 'OK'
    });
    request.approved = true;
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
 * Checks if a student has an active note-taking request for a specific course.
 */
const hasActiveNoteTakingRequest = (studentId: string, courseId: string): boolean => {
  const key = `${studentId}-${courseId}`;
  return !!noteTakingRequests.value[key];
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
 * Toggles dropdown for the selected student.
 */
 const toggleDropdown = (studentId: string, courseId: string) => {
  const dropdownKey = `${studentId}-${courseId}`;
  openDropdownId.value = openDropdownId.value === dropdownKey ? null : dropdownKey;
};


/**
 * Checks if the dropdown for a specific student is open.
 */
 const isDropdownOpen = (studentId: string, courseId: string) => {
  return openDropdownId.value === `${studentId}-${courseId}`;
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
  const professorId = route.params.professorId as string;
  await loadProfessor(professorId);
  await loadStudents(professorId);
  await loadNoteTakingRequestsForCourses(); 
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