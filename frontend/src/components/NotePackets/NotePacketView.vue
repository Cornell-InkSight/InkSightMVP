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
            <span :class="statusClass(notePacket.status as string)" class="text-sm font-semibold px-2 py-1 rounded-full">
                {{ notePacket.status }}
            </span>
        </div>

        <!-- Course Information -->
        <div class="mb-4 p-4 bg-white rounded-md shadow-sm">
            <h3 class="text-xl font-semibold text-gray-800">Course: {{ courseName }}</h3>
            <p class="text-gray-600">{{ notePacket.course_id }}</p>
        </div>

        <!-- Notes Content -->
        <div v-if="notePacket.notes && notePacket.notes.length" class="p-4 bg-white rounded-md shadow-sm">
            <h4 class="text-lg font-semibold text-gray-800 mb-3">Notes:</h4>
            <ul class="space-y-4">
                <li
                    v-for="note in notePacket.notes"
                    :key="note.id"
                    class="p-3 border-l-4 rounded-md shadow-sm"
                    :class="noteTypeClass(note.type)"
                >
                    <!-- Render Text Notes -->
                    <p v-if="note.type === 'text'" class="text-gray-700">{{ note.value }}</p>

                    <!-- Render LaTeX Notes -->
                    <p v-else-if="note.type === 'latex'" class="font-mono text-gray-800 text-lg">
                        <span v-html="renderLatex(note.value)"></span>
                    </p>

                    <!-- Render Image Notes -->
                    <div v-else-if="note.type === 'image'" class="flex justify-center">
                        <img :src="note.url" alt="Image Note" class="max-w-xs rounded-md shadow-md" />
                    </div>

                    <!-- Unsupported Type -->
                    <p v-else class="text-red-500">Unsupported note type: {{ note.type }}</p>
                </li>
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
import { fetchNotePacket, fetchCourse } from "@/services/api/fetch";
import * as interfaces from "@/services/api/interfaces";
import { useRoute } from 'vue-router';
import 'katex/dist/katex.min.css';
import katex from 'katex';

const notePacket = ref<interfaces.NotesPacket | null>(null);
const loading = ref(true); // Loading state
const courseName = ref<String>("");
const route = useRoute();


/**
 * Fetches data for thhe given notepacket id and assigns it to 'notePacket'
 * Logs error message if request fails. Also fetches the professor for each course.
 * @param notepacket_id // the id of the given student, from route params
 * @returns {Promise<Void>} // A Promise that resolves when the data is fetched and assigned
 */
const fetchNotePacketData = async (notepacket_id: string) => {
    loading.value = true; 
    const { data, error } = await fetchNotePacket(notepacket_id);
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
 * Returns dynamic classes for different note types.
 * @param {string} type - Type of the note (text, latex, image).
 */
 const noteTypeClass = (type: string) => {
    switch (type) {
        case 'text':
            return 'border-blue-500 bg-blue-50';
        case 'latex':
            return 'border-green-500 bg-green-50';
        case 'image':
            return 'border-yellow-500 bg-yellow-50';
        default:
            return 'border-gray-300 bg-gray-50';
    }
};

/**
 * Renders LaTeX content using a LaTeX library like KaTeX.
 * Replace with any LaTeX renderer library setup.
 * @param {string} latex - The LaTeX string to render.
 */
const renderLatex = (latex: string) => {
    try {
        // Example for KaTeX: replace with your preferred library
        return window.katex.renderToString(latex, { throwOnError: false });
    } catch (error) {
        console.error('Failed to render LaTeX:', error);
        return latex;
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
}

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
    const note_packet_id = route.params.notepacketId as string;
    await fetchNotePacketData(note_packet_id);
    if(notePacket) {
        const notePacketCourse = notePacket.value.course_id as string
        loadCourseName(notePacketCourse);
    }
});
</script>
