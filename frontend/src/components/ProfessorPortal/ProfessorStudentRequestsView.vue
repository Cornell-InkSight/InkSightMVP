<template>
<div class="p-4">
    <ul class="space-y-4">
    <li
        v-for="student in students"
        :key="student.user_ptr_id"
        class="flex items-center justify-between bg-white rounded-lg p-4 border hover:shadow-lg transition-shadow duration-300"
        :class="{
        'border-green-500': isApprovedNoteTakingRequest(student.user_ptr_id, course.id.toString()),
        'border-yellow-500': hasActiveNoteTakingRequest(student.user_ptr_id, course.id.toString()) && !isApprovedNoteTakingRequest(student.user_ptr_id, course.id.toString()),
        }"
    >
        <!-- Student Information -->
        <div class="flex items-center gap-4 cursor-pointer" @click="toggleDropdown(student.user_ptr_id, course.id.toString())">
        <div
            class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-200 text-gray-600 font-semibold text-lg"
        >
            {{ student.name.charAt(0) }}
        </div>
        <div>
            <p class="font-bold text-gray-800 text-lg">{{ student.name }}</p>
            <p class="text-sm text-gray-500">{{ student.disability }}</p>
        </div>
        </div>

        <!-- Request Status and Action -->
        <div v-if="hasActiveNoteTakingRequest(student.user_ptr_id, course.id.toString())" class="flex items-center gap-4">
        <div>
            <span
            class="px-2 py-1 text-xs rounded-full font-medium"
            :class="{
                'bg-green-100 text-green-800': isApprovedNoteTakingRequest(student.user_ptr_id, course.id.toString()),
                'bg-yellow-100 text-yellow-800': !isApprovedNoteTakingRequest(student.user_ptr_id, course.id.toString()),
            }"
            >
            {{ isApprovedNoteTakingRequest(student.user_ptr_id, course.id.toString()) ? 'Approved' : 'Pending' }}
            </span>
        </div>
        <button
            v-if="!isApprovedNoteTakingRequest(student.user_ptr_id, course.id.toString())"
            @click="approveRequest(student.user_ptr_id, course.id.toString())"
            class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white text-sm font-medium rounded-lg transition-colors duration-200"
        >
            Approve
        </button>
        </div>

        <!-- Dropdown with Details -->
        <div
        v-if="isDropdownOpen(student.user_ptr_id, course.id.toString())"
        class="absolute top-full left-0 mt-2 w-full bg-white border border-gray-200 rounded-lg p-4 z-10"
        >
        <p class="text-sm text-gray-700 mb-2">
            <strong>Status:</strong>
            {{ isApprovedNoteTakingRequest(student.user_ptr_id, course.id.toString()) ? 'Approved' : 'Pending approval' }}
        </p>
        <p class="text-sm text-gray-700">
            <strong>Request Details:</strong> {{ getRequestTooltip(student.user_ptr_id, course.id.toString()) }}
        </p>
        </div>
    </li>
    </ul>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { fetchStudentsForProfessors, fetchProfessor, fetchNotetakingRequestsForCourses, fetchCourse, fetchStudentCourses, fetchNoteTakingRequestStudentForCourse, fetchStudentsForProfessorCourse } from '@/services/api/fetch';
import { approveNoteTakingRequest } from "@/services/api/add";
import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue"
import { useUserStore } from "@/stores/authStore";
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

const props = defineProps({
    course: {
        type: Object,
        required: true,
    },
});


/**
 * Fetches students and courses for a specific professor by ID and assigns them to `studentscourses`.
 */
const loadStudents = async (courseId: string): Promise<void> => {
    const { data, error: fetchError } = await fetchStudentsForProfessorCourse(courseId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
        return;
    }
    students.value = data;
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
 * Loads note-taking requests for each course and populates `noteTakingRequests`.
 */
const loadNoteTakingRequestsForCourses = async () => {
    const { data, error: requestsError } = await fetchNotetakingRequestsForCourses(props.course.id);
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
    await loadStudents(props.course.id);
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