<template>
<div class="p-6 max-w-5xl mx-auto bg-gray-100 min-h-screen">
    <!-- Back Button -->
    <button @click="$emit('closePortal')" class="text-blue-500 mb-4">&larr; Back to classes</button>
    
    <!-- Course Name -->
    <h1 class="text-3xl font-bold mb-4">{{ selectedProfessorCourseStore.selectedCourse.name }}</h1>

    <!-- Broadcast Section -->
    <BroadcastView :courseId="selectedProfessorCourseStore.selectedCourse.id" :upoloadedSlideId="upoloadedSlideId" />

    <!-- Upload Slides Section -->
    <div class="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">Upload Slides</h2>
        <p class="text-sm text-gray-600 mb-6">Share lecture slides with your students. Supported formats: PDF, PowerPoint.</p>
        
        <input 
            type="file" 
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:border-blue-300" 
            @change="handleFileUpload"
            accept=".pdf, .ppt, .pptx"
        />
        <button
            class="mt-4 px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-md font-medium transition"
            @click="uploadSlides"
        >
            Upload
        </button>

        <!-- Uploaded Files Display -->
        <div v-if="uploadedSlides.length" class="mt-6">
            <h3 class="text-lg font-semibold mb-2 text-gray-800">Uploaded Slides</h3>
            <ul class="list-disc pl-5 text-gray-700">
                <li v-for="(slide, index) in uploadedSlides" :key="index" class="mb-2">
                    {{ slide.name }} - <a :href="slide.url" target="_blank" class="text-blue-500 hover:underline">View</a>
                </li>
            </ul>
        </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { fetchCourse } from "@/services/api/fetch"
import { uploadSlidesForLecture } from "@/services/api/add"
import BroadcastView from '@/components/Streaming/BroadcastView.vue';
import authAxios from '@/services/api/setup';
import Swal from 'sweetalert2';
import { useSelectedProfessorCourseStore } from "@/stores/selectedProfessorCourseStore"

const emit = defineEmits(['closePortal']);  

const uploadedSlides = ref<{ name: string, url: string }[]>([]); // Track uploaded slides
const selectedFile = ref<File | null>(null); // Store the selected file
const upoloadedSlideId = ref<string>();
const selectedProfessorCourseStore = useSelectedProfessorCourseStore(); // For interactive professor navbar

/**
 * Handle file selection
 */
const handleFileUpload = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        selectedFile.value = target.files[0];
    }
}

/**
 * Upload The Slides to AWS S3, Returns an error if upload unsuccessful, returns Sweet Alert if upload successful
 */
const uploadSlides = async () => {
    if (!selectedFile.value) {
        alert("Please select a file before uploading.");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile.value);

    try {
        const data = await uploadSlidesForLecture(selectedProfessorCourseStore.selectedCourse.id, formData);

        Swal.fire({
            title: 'File Uploaded',
            text: `The file has been uploaded..`,
            icon: 'success',
            confirmButtonText: 'OK'
        });

        selectedFile.value = null;
        upoloadedSlideId.value = data.slides.id;
    } catch (error) {
        alert(error.message || "An unexpected error occurred while uploading slides.");
    }
};

/**
 * Lifecycle hook called when the component is mounted.
 */
onMounted(async () => {
})
</script>
    