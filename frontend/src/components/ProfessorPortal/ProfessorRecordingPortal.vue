<template>
<div class="p-6 max-w-5xl mx-auto bg-gray-100 min-h-screen">
    <button @click="$emit('closePortal')" class="text-blue-500 mb-4">&larr; Back to classes</button>
    
    <h1 class="text-3xl font-bold mb-4">{{ courseName }}</h1>
    <BroadcastView :courseId="courseId" />
</div>
</template>
    
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { fetchCourse } from "@/services/api/fetch"
import BroadcastView from '@/components/Streaming/BroadcastView.vue';
import ProfessorPortalNavbar from '@/components/ProfessorPortal/ProfessorPortalNavbar.vue';

const props = defineProps<{ courseId: string }>();  
const emit = defineEmits(['closePortal']);  
const courseName = ref<String>();


/**
 * Gets the mode of the camera
 * @param facingMode // the way the camera is facing
 */
 async function getCameraStream(facingMode) {
    logAvailableCameras();
    try {
        return await navigator.mediaDevices.getUserMedia({
            video: { facingMode: { exact: facingMode } }, 
            audio: true,
        });
    } catch (error) {
        if (error.name === "OverconstrainedError") {
            console.warn(`Requested facing mode '${facingMode}' is not available. Falling back to default.`);
            return await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        } else {
            throw error;
        }
    }
}

/**
 * Logs available video input devices
 */
async function logAvailableCameras() {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(device => device.kind === "videoinput");
    console.log("Available cameras:", videoDevices);
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
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
onMounted(async () => {
    loadCourseName(props.courseId);
})
</script>
    