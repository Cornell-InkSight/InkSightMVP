<template>
<!-- Notes Packets -->
<div v-if="notePackets && notePackets.length > 0" class="space-y-4">
    <div
    v-for="packet in notePackets"
    :key="packet.id"
    class="flex items-center justify-between p-4 bg-white rounded-lg hover transition-all duration-300 border border-gray-200"
    >
    <!-- Left Content: Icon and Details -->
    <router-link :to="`/notepackets/${packet.id}/edit`" target="_blank" class="flex items-center space-x-4">
        <div class="w-12 h-16 bg-gray-100 rounded-md flex items-center justify-center">
        <i class="fas fa-file-alt text-gray-400 text-2xl"></i>
        </div>
        <div>
        <h4 class="text-lg font-semibold text-gray-900">Study Guide: Lecture {{ packet.lectureData.id }}</h4>
        <p class="text-sm text-gray-500">{{ packet.lectureData.date }}</p>
        </div>
    </router-link>

    <!-- Right Content: Actions -->
    <div class="flex items-center space-x-4">
        <!-- Publish Button -->
        <button
        @click="openPublishModal(packet)"
        class="bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium py-2 px-4 rounded-lg transition-colors"
        >
        Publish
        </button>
        <!-- Menu Icon -->
        <button class="text-gray-500 hover:text-gray-700">
        <i class="fas fa-ellipsis-v"></i>
        </button>
    </div>
    </div>
</div>

<!-- No Notes Packets Available -->
<p v-else class="text-center text-gray-500">No recent notes packets available.</p>

<!-- Publish Modal -->
<div v-if="showPublishModal" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md">
    <h3 class="text-lg font-bold text-gray-800 mb-4">Publish Notes Packet</h3>
    <p class="text-sm text-gray-600 mb-6">Are you sure you want to publish <strong>{{ selectedPacket.name || 'this packet' }}</strong>?</p>
    <div class="flex justify-end space-x-4">
        <button
        @click="showPublishModal = false"
        class="px-4 py-2 text-gray-600 hover:text-gray-800 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
        >
        Cancel
        </button>
        <button
        @click="publishPacket(selectedPacket)"
        class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
        Publish
        </button>
    </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { fetchdNotePacketsForCourse, fetchLectureSessionData } from "@/services/api/fetch";
import { ref, onMounted } from 'vue';
import { updateStatusOfNotePacket } from '@/services/api/add';
import { fetchCoursesForProfessors, fetchApprovedStudentsForCourse, fetchUnpublishedNotePacketsForCourse } from '@/services/api/fetch';
import { useRoute } from 'vue-router';
import * as interfaces from "@/services/api/interfaces";
import { useUserStore } from "@/stores/authStore";


const props = defineProps({
    course: {
        type: Object,
        required: true,
    },
});

const addNotesPacketsError = ref<string>(""); // Error

const showPublishModal = ref(false);
const selectedPacket = ref<any>(null);


// Input for New Notes Session
const newNotesSession = ref({
    lecture_session_id: "",
    course_id: 0,
    notes: "",
    status: "draft",
});
const approvedStudents = ref<Record<number, interfaces.Student[]>>({}); // List of Approved Students for course
const notePackets = ref<interfaces.NotesPacket[]>(); // List of notes packets for course


const showAddNotesPacketForm = ref(false); // checks if the add notes packet toggle is open or not
const selectedCourseId = ref<number | null>(null); // ID of the selected course


/**
 * Opens the publish modal and sets the selected packet.
 */
const openPublishModal = (packet: any) => {
selectedPacket.value = packet;
showPublishModal.value = true;
};

/**
 * Publishes the selected packet.
 */
const publishPacket = async (packet: any) => {
console.log(`Publishing packet: ${packet.id}`);
showPublishModal.value = false;
// Add API integration here to publish the packet
};

/**
 * Loads data for lecture session
 * @param lecture_session_id 
 */
const loadLectureSessionData = async (lecture_session_id: string) => {
    const { data, error: returnError } = await fetchLectureSessionData(lecture_session_id);
    if(returnError) {
        console.error(returnError);
    }
    return data;
}

/**
 * Loads the notepackets for a specific course
 * @param courseId - the ID of the course whose notespackets to load
 */
const loadNotesPacketsForCourse = async (courseId: number) => {
    const { data, error } = await fetchdNotePacketsForCourse(courseId.toString());
    if (error) {
        console.error(error);
        addNotesPacketsError.value = "Failed to load note packets";
        return [];
    }
    notePackets.value = await Promise.all(
        data.map(async (packet) => {
            const lectureData = await loadLectureSessionData(packet.lecture_session_id);
            return {
                ...packet, 
                lectureData,
            };

        })
    );
}

// /**
//  * Loads data for professor from API
//  * @param professorId - ID of the professor 
//  */
// const loadCoursesForProfessor = async (professorId: string) => {
//     const { data, error } = await fetchCoursesForProfessors(professorId);
//     if (error) {
//         console.error(error);
//         addNotesPacketsError.value = "Failed to load courses.";
//         return;
//     }
//     courses.value = data;
// };


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
    await loadNotesPacketsForCourse(props.course.id)
});
</script>

    
        