<template>
<div class="max-w-6xl mx-auto p-6 bg-gray-100 min-h-screen">
    <!-- Header with Title and Layout Options -->
    <div class="flex items-center justify-between mb-6">
    <h1 class="text-3xl font-bold text-gray-900">
        Classes for <span v-if="student">{{ student.name }}</span>
    </h1>
    </div>

    <!-- Note Taking Request Form -->
    <div class="bg-white p-4 rounded-lg shadow-md mb-6">
    <h2 class="text-xl font-bold mb-4">Add Note-Taking Request</h2>

    <!-- Form for Adding Note-Taking Request -->
    <form @submit.prevent="submitNoteTakingRequest">
        <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">Course</label>
        <select 
            v-model="selectedCourseId" 
            class="mt-1 p-2 block w-full border border-gray-300 rounded-md" 
            required
        >
            <option value="" disabled>Select a course</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">
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
        class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
    >
        <h2 class="text-xl font-bold text-gray-800">{{ course.name }}</h2>
        <p class="text-gray-600">{{ course.description }}</p>
        <p class="mt-2 text-sm text-gray-500">{{ course.instructor }}</p>
    </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { fetchStudent, fetchCourses } from "@/services/api/fetch";
import { addNoteTakingRequest } from "@/services/api/add";

const route = useRoute();
const studentId = route.params.studentId as string;

const courses = ref<any[]>([]);  // Holds data for student's courses
const student = ref<any | null>(null);  // Holds data for student
const loading = ref<boolean>(true);  // Loading state indicator
const error = ref<string | null>(null);  // Error message, if any
const selectedCourseId = ref<string>("");  // Selected course ID from the dropdown
const noteTakingRequest = ref<string>("");  // Note-taking request details from the form
const submitSuccessMessage = ref<string | null>(null);  // Success message on submission
const submitErrorMessage = ref<string | null>(null);  // Error message on submission

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
const loadCourses = async () => {
    const { data, error: coursesError } = await fetchCourses(studentId);
    if (coursesError) {
        error.value = coursesError;
    } else {
        courses.value = data;
    }
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
    } catch (error) {
        console.error("Error adding note-taking request:", error);
        submitErrorMessage.value = "Failed to add note-taking request. Please try again.";
    }
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for the student and their courses.
 */
onMounted(async () => {
    await loadStudent();
    await loadCourses();
    loading.value = false; 
});
</script>


