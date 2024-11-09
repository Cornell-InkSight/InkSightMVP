<template>
    <ProfessorPortalNavbar />
    <div class="p-6 max-w-4xl mx-auto bg-white rounded-lg shadow-md">
        <h1 class="text-2xl font-bold mb-4">Courses</h1>

        <!-- Error Message -->
        <div v-if="addLectureSessionError" class="text-red-500 mb-4">
            {{ addLectureSessionError }}
        </div>

        <!-- Courses Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="course in courses" :key="course.id" class="p-4 bg-white rounded-lg shadow-md border border-gray-200">
                <h2 class="text-lg font-semibold">{{ course.name }}</h2>
                <p class="text-sm text-gray-600">{{ course.description }}</p>
                
                <!-- Add Button to Open Lecture Form -->
                <button 
                    @click="toggleLectureForm(course.id)" 
                    class="mt-4 bg-gray-300 text-gray-700 py-2 px-4 rounded-full hover:bg-gray-400"
                >
                    + Publish Notes
                </button>

                <!-- Lecture Session Form (Visible only for the selected course) -->
                <div v-if="showAddLectureSessionForm && selectedCourseId === course.id" class="mt-4 border-t pt-4">
                    <h3 class="text-lg font-semibold mb-2">Add Lecture Session</h3>
                    <form @submit.prevent="loadAddLectureSession(professorId)">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700" for="date">Date</label>
                            <input 
                                v-model="newLectureSession.date" 
                                type="date" 
                                id="date" 
                                class="mt-1 p-2 block w-full border rounded-md"
                                required
                            />
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700" for="notepacket">Notes Packet</label>
                            <input 
                                v-model="newLectureSession.notepacket" 
                                type="text" 
                                id="notepacket" 
                                placeholder="Enter notes packet"
                                class="mt-1 p-2 block w-full border rounded-md"
                                required
                            />
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700" for="status">Status</label>
                            <input 
                                v-model="newLectureSession.status" 
                                type="text" 
                                id="status" 
                                placeholder="Enter status"
                                class="mt-1 p-2 block w-full border rounded-md"
                                required
                            />
                        </div>
                        <button 
                            type="submit" 
                            class="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
                        >
                            Add Lecture Session
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { addLectureSession } from '@/services/api/add';
import { fetchCoursesForProfessors } from '@/services/api/fetch';
import { useRoute } from 'vue-router';
import * as interfaces from "@/services/api/interfaces";
import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue"

const courses = ref<interfaces.Course[]>([]);
const addLectureSessionError = ref<string>("");
const newLectureSession = ref<interfaces.LectureSession>({
    date: '',
    course_id: 0,
    notepacket: "",
    status: ""
});
const route = useRoute();
const professorId = route.params.professorId as string;

const showAddLectureSessionForm = ref(false);
const selectedCourseId = ref<number | null>(null); // Track which course form to show

/**
 * Toggles the lecture session form for the selected course.
 * @param {number} courseId - The ID of the selected course.
 */
const toggleLectureForm = (courseId: number) => {
    if (selectedCourseId.value === courseId) {
        // If the form is already open for this course, close it
        showAddLectureSessionForm.value = false;
        selectedCourseId.value = null;
    } else {
        // Open the form for the selected course
        showAddLectureSessionForm.value = true;
        selectedCourseId.value = courseId;
        newLectureSession.value.course_id = courseId; // Set the course_id in the lecture session
    }
};

/**
 * Loads and adds a lecture session for the selected course.
 * Ensures all fields are filled and refreshes course list.
 */
const loadAddLectureSession = async (professorId: string) => {
    const { date, course_id, notepacket, status } = newLectureSession.value;

    if (!date || !course_id || !notepacket || !status) {
        addLectureSessionError.value = "All fields are required.";
        return;
    }

    const lecturesession = { date, course_id, notepacket, status } as interfaces.LectureSession;
    const { error: addError } = await addLectureSession(lecturesession);

    if (addError) {
        addLectureSessionError.value = addError;
    } else {
        addLectureSessionError.value = "";
        showAddLectureSessionForm.value = false;
        newLectureSession.value = { date: '', course_id: 0, notepacket: "", status: "" };
        selectedCourseId.value = null; // Reset selected course
        loadCoursesForProfessor(professorId); // Refresh the course list
    }
};

/**
 * Fetches the courses for a specific professor.
 */
const loadCoursesForProfessor = async (professorId: string) => {
    const { data, error } = await fetchCoursesForProfessors(professorId);
    if (error) {
        console.error(error);
        addLectureSessionError.value = "Failed to load courses.";
        return;
    }
    courses.value = data;
};

onMounted(async () => {
    await loadCoursesForProfessor(professorId);
});
</script>
