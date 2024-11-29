<template>
<div class="max-w-4xl mx-auto p-6 bg-gray-100 rounded-lg shadow-lg mt-6">
    <!-- Loading State -->
    <div v-if="loading" class="text-center text-gray-500 animate-pulse">
        Loading notes packet...
    </div>

    <!-- Main Content -->
    <div v-else-if="notePacket">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-gray-900">
                Notes Packet For Lecture {{ notePacket.title }}
            </h2>
            <h4 class="text-2xl font-bold text-gray-900">
                Lecture {{ notePacket.lecture_session_id }}
            </h4>
        </div>

        <!-- Course Information -->
        <div class="mb-4 p-4 bg-white rounded-md shadow-sm">
            <h3 class="text-xl font-semibold text-gray-800">Student: {{ studentName }}</h3>
        </div>

        <!-- Notes Content -->
        <div v-if="notePacket.notes && Object.keys(notePacket.notes).length" class="p-4 bg-white rounded-md shadow-sm">
            <h4 class="text-lg font-semibold text-gray-800 mb-3">Notes:</h4>
            <ul class="space-y-2">
                <span class="font-medium text-gray-900">{{ notePacket.notes }} </span>
            </ul>
        </div>

        <!-- Empty State -->
        <div v-else class="text-gray-500 text-center">
            No notes available for this packet.
        </div>
    </div>

    <!-- Error State if notePacket is null -->
    <div v-else class="text-red-500 text-center">
        Error loading notes packet data.
    </div>
</div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchStudentNotePacket, fetchStudent } from "@/services/api/fetch";
import * as interfaces from "@/services/api/interfaces";
import { useRoute } from 'vue-router';

const notePacket = ref<interfaces.StudentNotePacket | null>(null);
const loading = ref(true); // Loading state
const studentName = ref<String>("");
const route = useRoute();


/**
 * Fetches data for thhe given notepacket id and assigns it to 'notePacket'
 * Logs error message if request fails. Also fetches the professor for each course.
 * @param notepacket_id // the id of the given student, from route params
 * @returns {Promise<Void>} // A Promise that resolves when the data is fetched and assigned
 */
const loadStudentNotePacketData = async (notepacket_id: string) => {
    loading.value = true; 
    const { data, error } = await fetchStudentNotePacket(notepacket_id);
    if (error) {
        console.error(error);
        return;
    }
    notePacket.value = data;
    loading.value = false; 
};

/**
 * Sets up dynamic styles for the status of the notepacket
 * @param status the status of the notespacket
 */
const statusClass = (status: string | undefined) => {
    switch (status) {
        case 'approved':
        return 'bg-green-100 text-green-700';
        case 'edits':
        return 'bg-yellow-100 text-yellow-700';
        case 'draft':
        return 'bg-gray-100 text-gray-600';
        default:
        return 'bg-gray-100 text-gray-600';
    }
};


/**
 * Loads course names for each course ID in `studentscourses`.
 */ 
const loadStudentName = async (studentId: string): Promise<void> => {
    const { data, error: fetchError } = await fetchStudent(studentId);
    if (!fetchError && data) {
        studentName.value = data.name;
    } else {
        console.error(`Failed to fetch course name for course ID ${studentId}:`, fetchError);
    }
}

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
    const note_packet_id = route.params.notepacketId as string;
    await loadStudentNotePacketData(note_packet_id);
    if(notePacket) {
        const notePacketStudent = notePacket.value.student_id as string
        loadStudentName(notePacketStudent);
    }
});
</script>
    