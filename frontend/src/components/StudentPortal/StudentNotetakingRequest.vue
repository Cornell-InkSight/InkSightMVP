<template>
<div class="flex min-h-screen bg-gray-100">
  <StudentPortalNavbar />
  <div class="p-6 bg-gray-100 min-h-screen">

    <!-- Header with Title and Layout Options -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-gray-900">
        Classes for <span v-if="student">{{ student.name }}</span>
      </h1>
    </div>

    <!-- Note Taking Request Form -->
    <div class="bg-white p-4 rounded-lg border border-black mb-6">
      <h2 class="text-xl font-bold mb-1">Add Note-Taking Request</h2>
      <h3 class="mb-4" v-if="sdscoordinator">SDS Coordinator: {{ sdscoordinator.name }}</h3>

      <form @submit.prevent="submitNoteTakingRequest">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Course</label>
          <select 
            v-model="selectedCourseId" 
            class="mt-1 p-2 block w-[90%] border border-gray-300 rounded-md" 
            required
          >
            <option value="" disabled>Select a course</option>
            <option v-for="course in dropdownCourses" :key="course.id" :value="course.id">
              {{ course.name }}
            </option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Request Details</label>
          <textarea 
            v-model="noteTakingRequest" 
            rows="4" 
            class="mt-1 p-2 block w-full border border-gray-300 rounded-md" 
            placeholder="Enter details of your request..." 
            required
          ></textarea>
        </div>

        <button 
          type="submit" 
          class="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
        >
          Submit Request
        </button>
      </form>

      <!-- Success/Error Message -->
      <div v-if="submitSuccessMessage" class="text-green-500 mt-4">
        {{ submitSuccessMessage }}
      </div>
      <div v-if="submitErrorMessage" class="text-red-500 mt-4">
        {{ submitErrorMessage }}
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
        class="p-4 bg-white rounded-lg border border-black"
        :class="{ 'border-l-4 border-green-500': isApprovedNoteTakingRequest(studentId, course.id), 'border-l-4 border-yellow-500': hasActiveNoteTakingRequest(studentId, course.id) && !isApprovedNoteTakingRequest(studentId, course.id) }"
      >
      <h2 class="text-xl font-bold text-gray-900 mb-2 w-[100%]">{{ course.name.split(": ")[0] }}</h2>
      <p class="text-sm text-gray-600">{{ course.name.split(": ")[1] }}</p>
        
        <!-- Professors Section -->
        <div v-if="course.professors && course.professors.length > 0" class="mt-2">
          <h4 class="text-sm font-semibold text-gray-700">Professors:</h4>
          <ul class="mt-1 space-y-1">
            <li v-for="professor in course.professors" :key="professor.user_ptr_id" class="text-sm text-gray-600 bg-gray-100 rounded-md p-2">
              {{ professor.name }}
            </li>
          </ul>
        </div>

        <!-- Display Note Taking Request if Exists for this Course -->
        <div v-if="noteTakingRequests[`${String(studentId)}-${String(course.id)}`]" class="mt-4 p-2 border-t border-gray-300">
          <h3 class="text-md font-semibold text-gray-700">Note-Taking Request:</h3>
          <p class="text-sm text-gray-600">{{ noteTakingRequests[`${String(studentId)}-${String(course.id)}`].request }}</p>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { fetchStudent, fetchCourses, fetchNotetakingRequestsForCourses, fetchStudentCourses, fetchSDSCoordinator, fetchProfessorsForCourses, fetchIsPendingStudentForCourse } from "@/services/api/fetch";
import * as interfaces from "@/services/api/interfaces";
import { addNoteTakingRequest } from "@/services/api/add";
import StudentPortalNavbar from '@/components/StudentPortal/StudentPortalNavbar.vue';
import { fetchIsApprovedStudentForCourse } from '../../services/api/fetch';

const route = useRoute();
const studentId = route.params.studentId as string;

const courses = ref<interfaces.Course[]>([]);
const dropdownCourses = ref<interfaces.Course[]>([]);
const student = ref<interfaces.Student | null>(null);
const loading = ref<boolean>(true);
const error = ref<string | null>(null);
const selectedCourseId = ref<string>("");
const noteTakingRequest = ref<string>("");
const sdscoordinator=ref<interfaces.SDSCoordinator>();
const submitSuccessMessage = ref<string | null>(null);
const submitErrorMessage = ref<string | null>(null);

// Dictionary to store note-taking requests by `studentId-courseId`
const noteTakingRequests = ref<Record<string, { approved: boolean; requestId: string, request: string }>>({}); // Tracks note-taking requests by `studentId-courseId` key with approval status

/**
 * Fetches data for the given student and assigns it to `student`.
 */
const loadStudent = async () => {
  const { data, error: studentError } = await fetchStudent(studentId);
  if (studentError) {
    error.value = studentError;
    return;
  } 
  student.value = data;
};

/**
 * Fetches data for the courses for the given student and assigns it to `courses`.
 */
 const loadCourses = async (studentId: string) => {
  const { data, error: coursesError } = await fetchCourses(studentId);
  if (coursesError) {
    error.value = coursesError;
  } else {
    const coursePromises = data.map(async (course: interfaces.Course) => {
      const professors = await loadProfessorsForCourses(course.id);
      const { data: pendingData, error: pendingError } = await fetchIsPendingStudentForCourse(studentId, course.id);
      const { data: isApprovedData, error: approvedError } = await fetchIsApprovedStudentForCourse(studentId, course.id);
      const cannotRequest = pendingData || isApprovedData
      return {
        ...course,
        professors,
        cannotRequest,
      };
    });
    courses.value = await Promise.all(coursePromises); 
    dropdownCourses.value = courses.value.filter(course => !course.cannotRequest);
  }
};


/**
 * Fetches professors for specific course
 * @param courseId ID of the Course to fetch professors
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
 * Fetches note-taking requests for the student's courses and populates `noteTakingRequests`.
 */
const loadNoteakingRequestsForCourses = async () => {
  courses.value.forEach(async course => {
    const { data, error: requestsError } = await fetchNotetakingRequestsForCourses(course.id);
    if (requestsError) {
      console.error(requestsError);
      error.value = requestsError;
    } else {
      data.forEach(async (request: any) => {
        let studentcourse = await fetchStudentCourses(request.student_course_id);
        const key = `${studentcourse.data.student_id}-${studentcourse.data.course_id}`;
        noteTakingRequests.value[key] = { approved: request.approved, requestId: request.id, request: request.request };
      });
    }
  })
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
 * Submits the note-taking request for the selected course.
 */
const submitNoteTakingRequest = async () => {
  submitSuccessMessage.value = null;
  submitErrorMessage.value = null;

  try {
    if (!selectedCourseId.value || !noteTakingRequest.value) {
      submitErrorMessage.value = "Please select a course and enter request details.";
      return;
    }
    await addNoteTakingRequest(studentId, selectedCourseId.value, noteTakingRequest.value);
    
    submitSuccessMessage.value = "Note-taking request added successfully!";
    
    selectedCourseId.value = "";
    noteTakingRequest.value = "";
    await loadNoteakingRequestsForCourses();
    await loadCourses(studentId);
  } catch (error) {
    console.error("Error adding note-taking request:", error);
    submitErrorMessage.value = "Failed to add note-taking request. Please try again.";
  }
};

/**
 * Load Student-Courses
 */
const loadStudentCourses = async (studentcourseId: string) => {
  const { data, error: fetchError } = await fetchStudentCourses(studentcourseId);
  if (fetchError) {
    console.error(fetchError);
    error.value = fetchError;
    return;
  }
  return data;
}

/**
 * Fetches the SDS Coordinator data for the given SDS Coordinator id and assigns to `sdscoordinator`
 * Logs error message if request fails
 * @param sdscoordinatorId // the id of the given SDS Coordinator from route params
 * @returns {Promise<void>} // A Promise that resolves when data is fetched and assigned
 */
const loadSDSCoordinator = async (sdscoordinatorId: string) => {
  const { data, error } = await fetchSDSCoordinator(sdscoordinatorId);
  if (error) {
      console.error(error);
      return;
  }
  sdscoordinator.value = data;
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for the student and their courses and their notetaking requests.
 */
onMounted(async () => {
  const studentId = route.params.studentId as string;
  await loadStudent();
  await loadCourses(studentId);
  await loadNoteakingRequestsForCourses();
  if(student) {
    await loadSDSCoordinator(student.value.sds_coordinator_id)
  }
  loading.value = false;
});
</script>
