<template>
<div class="p-6 max-w-5xl mx-auto bg-gray-100 min-h-screen">
    <button @click="$emit('closePortal')" class="text-blue-500 mb-4">&larr; Back to classes</button>
    
    <h1 class="text-3xl font-bold mb-4">{{ courseName }}</h1>
    
    <div class="flex gap-4 mb-4">
        <button
            v-if="!isRecording"
            @click="startRecording"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg"
        >
            Start Recording
        </button>
        <button
            v-if="isRecording"
            @click="stopRecording"
            class="px-4 py-2 bg-red-500 text-white rounded-lg"
        > 
            Stop Recording
        </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
    <!-- Live Camera View -->
    <div class="col-span-2">
        <div class="bg-black rounded-lg overflow-hidden relative">
        <img src="https://via.placeholder.com/800x450" alt="Live camera view" class="w-full h-full object-cover" />
        <span class="absolute bottom-2 left-2 bg-red-600 text-white text-sm px-2 py-1 rounded-full">🔴 Live camera view</span>
        </div>
    </div>
    
    <!-- Image to Text Notes -->
    <div>
        <h2 class="text-xl font-semibold mb-2">Image to text notes:</h2>
        <div class="bg-white p-4 rounded-lg shadow-md">
        <p id="notes-text" class="text-gray-700 mb-2">{{ fakeNote }}</p>
        <img src="https://via.placeholder.com/300x150" alt="Converted notes" class="rounded-lg mt-2" />
        </div>
    </div>
    </div>
    
    <!-- Captions Section -->
    <div class="mt-6">
    <h2 class="text-xl font-semibold mb-2">Captions</h2>
    <div class="bg-white p-4 rounded-lg shadow-md text-gray-700">
        In theory, we could use exact methods to calculate the best actions the robot should take from every possible position in the maze.
        <br/><br/>
        However, if the maze is enormous, this quickly becomes impractical as it would take forever to compute.
    </div>
    </div>
</div>
</template>
    
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { faker } from '@faker-js/faker';
import { fetchCourse } from "@/services/api/fetch"
import { addNewLectureSession, addNewNotesPacket } from "@/services/api/add"
import { updateStatusOfLecture } from "@/services/api/add"

const props = defineProps<{ courseId: string }>();  
const emit = defineEmits(['closePortal']);  
const courseName = ref<String>();

const isRecording = ref(false); 
const lectureSessionId = ref<string | null>(null);
const fakeNote = ref<string>(faker.lorem.paragraph(2)); // Generate a fake note using faker

/**
 * Starts the recording, creates new lecture in the API and calls the POST API
 */
const startRecording = async () => {
    try {
        const lectureSessionData = {
            date: new Date(),
            course_id: props.courseId,
            status: "recording",
            url: "https://example.com/stream-url" 
        };
        
        const response = await addNewLectureSession(lectureSessionData);
        
        lectureSessionId.value = response.id;
        isRecording.value = true;
        console.log("Lecture session started:", response);
    } catch (error) {
        console.error("Failed to start recording:", error);
    }
}

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
 * Ends recording, uploads new notes packet to the API
 */
const stopRecording = async () => {
    if (!lectureSessionId.value) return; 
    const notes_packet_data = {
        "lecture_session_id": lectureSessionId.value,
        "course_id": props.courseId,
        "notes": fakeNote.value, // Use the generated fake note
        "status": "draft",
    }
    addNewNotesPacket(notes_packet_data)
    try {
        const response = await updateStatusOfLecture(lectureSessionId.value, "done");
        isRecording.value = false;
        console.log("Lecture session stopped:", response);
    } catch (error) {
        console.error("Failed to stop recording:", error);
    }
}

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
    loadCourseName(props.courseId);
})
</script>
    