<template>
<div class="flex min-h-screen bg-gray-100">
    <ProfessorPortalNavbar />
    <div class="p-6 bg-gray-100 min-h-screen w-[80%]">
    <h1 class="text-2xl font-bold mb-4">Courses</h1>

    <!-- Error Message -->
    <div v-if="addNotesPacketsError" class="text-red-500 mb-4">
    {{ addNotesPacketsError }}
    </div>

    <!-- Courses Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
    <div v-for="course in courses" :key="course.id" class="p-4 bg-white rounded-lg shadow-md border border-gray-200">
        <h2 class="text-lg font-semibold">{{ course.name }}</h2>
        <!-- <p class="text-sm text-gray-600">{{ course.description }}</p> -->
        
        <!-- Add Button to Open Notes Packet Form -->
        <button 
        @click="toggleNotesPacketForm(parseInt(course.id))" 
        class="mt-4 bg-gray-300 text-gray-700 py-2 px-4 rounded-full hover:bg-gray-400"
        >
        + Notes
        </button>

        <!-- Notes Packet Section -->
        <div v-if="showAddNotesPacketForm && notePackets[course.id]" class="mt-6">
        <h3 class="text-lg font-semibold mb-2">Edit New Notes Packets</h3>
        <ul class="space-y-2">
            <li v-for="(packet, index) in [...notePackets[course.id]].reverse().slice(0, 5)" :key="packet.id">
            <router-link :to="`/notepackets/${packet.id}/edit`" target="_blank" class="text-blue-500 hover:underline">
                Lecture Session {{ packet.lecture_session_id }}
            </router-link>
            </li>
        </ul>
        </div>

        <!-- Notes Packet Form (Visible only for the selected course) -->
        <div v-if="showAddNotesPacketForm && selectedCourseId == Number(course.id)" class="mt-4 border-t pt-4">
        <h3 class="text-lg font-semibold mb-2">Publish Notes</h3>
        <form @submit.prevent="submitNotesPacketForm">
            
            <!-- Notes Packet Dropdown -->
            <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700" for="notepacket">Notes Packet</label>
            <select 
                v-model="newNotesSession.lecture_session_id" 
                id="notepacket" 
                class="mt-1 p-2 block w-full border rounded-md"
                required
            >
                <option v-if="!notePackets[course.id]" disabled>Loading...</option>
                <option v-for="packet in notePackets[course.id]" :key="packet.id as string" :value="packet.id">
                Packet from Lecture Session {{ packet.lecture_session_id }}
                </option>
            </select>
            </div>

            <button 
            type="submit" 
            class="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
            >
            Publish Notes
            </button>
        </form>

        <!-- Approved Students List -->
        <div class="mt-6">
            <h4 class="text-md font-semibold text-gray-700">Approved Students for Note Packets</h4>
            <ul v-if="approvedStudents[course.id]" class="mt-2 space-y-1">
            <li v-for="student in approvedStudents[course.id]" :key="student.id" class="text-gray-600">
                <span class="text-sm">{{ student.name }}</span>
            </li>
            </ul>
            <p v-else class="text-sm text-gray-500">No approved students for this course.</p>
        </div>
        </div>
    </div>
    </div>
</div> 
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { updateStatusOfNotePacket } from '@/services/api/add';
import { fetchCoursesForProfessors, fetchApprovedStudentsForCourse, fetchUnpublishedNotePacketsForCourse } from '@/services/api/fetch';
import { useRoute } from 'vue-router';
import * as interfaces from "@/services/api/interfaces";
import ProfessorPortalNavbar from "@/components/ProfessorPortal/ProfessorPortalNavbar.vue"
import { useUserStore } from "@/stores/authStore";

const courses = ref<interfaces.Course[]>([]); // List of Professors Courses
const addNotesPacketsError = ref<string>(""); // Error

// Input for New Notes Session
const newNotesSession = ref({
    lecture_session_id: "",
    course_id: 0,
    notes: "",
    status: "draft",
});
const approvedStudents = ref<Record<number, interfaces.Student[]>>({}); // List of Approved Students for course
const notePackets = ref<Record<number, interfaces.NotesPacket[]>>({}); // List of notes packets for course

const route = useRoute(); // router for params
const professorId = route.params.professorId as string; // professor ID for respective page

const showAddNotesPacketForm = ref(false); // checks if the add notes packet toggle is open or not
const selectedCourseId = ref<number | null>(null); // ID of the selected course

/**
 * Toggles the Note Packets Form for the specific course
 * @param courseId 
 */
 const toggleNotesPacketForm = async (courseId: number) => {
    if (selectedCourseId.value === courseId) {
        showAddNotesPacketForm.value = false;
        selectedCourseId.value = null;
    } else {
        showAddNotesPacketForm.value = true;
        selectedCourseId.value = courseId;
        newNotesSession.value.course_id = courseId;

        if (!approvedStudents.value[courseId]) {
            const students = await loadApprovedStudentsForCourse(courseId);
            approvedStudents.value[courseId] = students || [];
        }

        if (!notePackets.value[courseId]) {
            const packets = await loadNotesPacketsForCourse(courseId);
            notePackets.value[courseId] = packets || [];
        }
    }
};


/**
 * Loads data for professor from API
 * @param professorId - ID of the professor 
 */
const loadCoursesForProfessor = async (professorId: string) => {
    const { data, error } = await fetchCoursesForProfessors(professorId);
    if (error) {
        console.error(error);
        addNotesPacketsError.value = "Failed to load courses.";
        return;
    }
    courses.value = data;
};

/**
 * Loads the notepacket for a specific course
 * @param courseId - the ID of the course whose notespackets to load
 */
const loadNotesPacketsForCourse = async (courseId: number) => {
    const { data, error } = await fetchUnpublishedNotePacketsForCourse(courseId.toString());
    if (error) {
        console.error(error);
        addNotesPacketsError.value = "Failed to load note packets";
        return [];
    }
    return data;
};

/**
 * Loads the approved students for the course
 * @param courseId - the ID of the course
 */
const loadApprovedStudentsForCourse = async (courseId: number) => {
    const { data, error } = await fetchApprovedStudentsForCourse(courseId.toString());
    if (error) {
        console.error(error);
        return [];
    }
    return data;
};

/**
 * Submit A New Published Note Packet
 * Updates status of notepacket to published, resets form values
 */
const submitNotesPacketForm = async () => {
    if (!newNotesSession.value.lecture_session_id) {
        addNotesPacketsError.value = "Please select a notes packet.";
        return;
    }

    const { error } = await updateStatusOfNotePacket(newNotesSession.value.lecture_session_id, "published");
    if (error) {
        console.error(error);
        addNotesPacketsError.value = "Failed to publish notes packet.";
    } else {
        addNotesPacketsError.value = "";
        showAddNotesPacketForm.value = false;
        selectedCourseId.value = null; 
    }
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their courses.
 */
onMounted(async () => {
    const userStore = useUserStore()
    await userStore.fetchUser()
    const user = userStore.user;
    const professorId = user.user_ptr_id;
    await loadCoursesForProfessor(professorId);
});
</script>
  