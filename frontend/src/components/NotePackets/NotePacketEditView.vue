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
                Notes Packet For Lecture {{ notePacket.lecture_session_id }}
            </h2>
            <span :class="statusClass(notePacket.status)" class="text-sm font-semibold px-2 py-1 rounded-full">
                {{ notePacket.status }}
            </span>
        </div>

        <!-- Course Information -->
        <div class="mb-4 p-4 bg-white rounded-md shadow-sm">
            <h3 class="text-xl font-semibold text-gray-800">Course: {{ courseName }}</h3>
            <p class="text-gray-600">{{ notePacket.course?.code }}</p>
        </div>

        <!-- Notes Content -->
        <div class="p-4 bg-white rounded-md shadow-sm">
            <h4 class="text-lg font-semibold text-gray-800 mb-3">Notes:</h4>
            <textarea v-model="updatedText" class="w-full p-2 border border-gray-300 rounded-md" rows="6"></textarea>
            <div class="flex justify-end mt-4">
                <button 
                    @click="updateText" 
                    :disabled="isUpdating"
                    class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                    {{ isUpdating ? "Updating..." : "Save Changes" }}
                </button>
            </div>
            <p v-if="updateMessage" class="text-center mt-4" :class="updateMessageClass">
                {{ updateMessage }}
            </p>
        </div>
    </div>

    <!-- Error State if notePacket is null -->
    <div v-else class="text-red-500 text-center">
        Error loading notes packet data.
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { fetchNotePacket, fetchCourse } from "@/services/api/fetch";
import { updateTextOfNotePacket } from "@/services/api/add";
import * as interfaces from "@/services/api/interfaces";
import { useRoute } from 'vue-router';

const notePacket = ref<interfaces.NotesPacket | null>(null);
const loading = ref(true); // Loading state
const courseName = ref<String>("");
const route = useRoute();

// New reactive variables for updating
const updatedText = ref<string>(""); // Holds updated text content
const isUpdating = ref<boolean>(false); // Indicates if update request is in progress
const updateMessage = ref<string | null>(null); // Holds update status message

/**
 * Fetches data for the given notepacket id and assigns it to 'notePacket'.
 * Also initializes 'updatedText' with the current notes content.
 */
const fetchNotePacketData = async (notepacket_id: string) => {
    loading.value = true; 
    const { data, error } = await fetchNotePacket(notepacket_id);
    if (error) {
        console.error(error);
        return;
    }
    notePacket.value = data;
    updatedText.value = data.notes || ""; // Initialize updatedText with existing notes
    loading.value = false; 
};

/**
 * Updates the text content of the note packet by calling the updateTextOfNotePacket function.
 */
const updateText = async () => {
    if (!notePacket.value) return;
    
    isUpdating.value = true;
    updateMessage.value = null; // Clear previous message

    try {
        await updateTextOfNotePacket(notePacket.value.id, updatedText.value);
        updateMessage.value = "Text updated successfully!";
    } catch (error: any) {
        console.error(error.message);
        updateMessage.value = "Failed to update text. Please try again.";
    } finally {
        isUpdating.value = false;
    }
};

/**
 * Sets up dynamic styles for the status of the note packet
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
const loadCourseName = async (courseId: string): Promise<void> => {
    const { data, error: fetchError } = await fetchCourse(courseId);
    if (!fetchError && data) {
        courseName.value = data.name;
    } else {
        console.error(`Failed to fetch course name for course ID ${courseId}:`, fetchError);
    }
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
    const note_packet_id = route.params.notepacketId as string;
    await fetchNotePacketData(note_packet_id);
    if (notePacket.value) {
        loadCourseName(notePacket.value.course_id);
    }
});

/**
 * Computed class for update message styling.
 */
const updateMessageClass = computed(() => {
    return updateMessage.value === "Text updated successfully!" ? "text-green-500" : "text-red-500";
});
</script>
