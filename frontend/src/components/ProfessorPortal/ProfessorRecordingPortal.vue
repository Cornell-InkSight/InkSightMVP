<template>
<div class="p-6 max-w-5xl mx-auto bg-gray-100 min-h-screen">
    <!-- Back Button -->
    <button @click="$emit('closePortal')" class="text-blue-500 mb-4">&larr; Back to classes</button>
    
    <!-- Course Name -->
    <h1 class="text-3xl font-bold mb-4">{{ courseName }}</h1>

    <!-- Broadcast Section -->
    <BroadcastView :courseId="courseId" />
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { fetchCourse } from "@/services/api/fetch"
import BroadcastView from '@/components/Streaming/BroadcastView.vue';

const props = defineProps<{ courseId: string }>();  
const emit = defineEmits(['closePortal']);  

const courseName = ref<String>();

/**
 * Fetch course name
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
 */
onMounted(async () => {
    loadCourseName(props.courseId);
})
</script>
    