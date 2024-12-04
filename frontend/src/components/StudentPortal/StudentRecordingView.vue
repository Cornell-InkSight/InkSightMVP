<template>
<div class="flex min-h-screen">
    <StudentPortalNavbar />
    <div class="w-[85%] p-6 bg-gray-100 min-h-screen">
        <!-- Main Page -->
            <!-- Course Title -->
            <div class="flex items-center justify-between">
                <h1 class="text-3xl font-bold mb-4">{{ courseName }}</h1>
                <span v-if="isRecording" class="bg-red-600 text-white text-sm px-3 py-1 rounded-full">
                    🔴 Live
                </span>
            </div>

            <!-- Viewer -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="col-span-2 bg-black rounded-lg overflow-hidden">
                    <ViewerVue/>
                </div>

                <!-- Image to Text Notes -->
                <div>
                    <h2 class="text-xl font-semibold mb-2">Image to text notes:</h2>
                    <div class="width-[50%] bg-white p-4 rounded-lg shadow-md">
                        <p id="notes-text" class="text-gray-700 mb-2">{{ fakeNote }}</p>
                        <img src="https://via.placeholder.com/300x150" alt="Converted notes" class="rounded-lg mt-2" />
                    </div>
                </div>
            </div>
            
            <!-- Captions Section -->
            <div class="mt-6">
                <h2 class="text-xl font-semibold mb-2">Captions</h2>
                <div class="bg-white p-4 rounded-lg shadow-md text-gray-700">
                    <p>
                        In theory, we could use exact methods to calculate the best actions the robot should take from every possible position in the maze.
                        <br /><br />
                        However, if the maze is enormous, this quickly becomes impractical as it would take forever to compute.
                    </p>
                </div>
            </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { faker } from '@faker-js/faker';
import ViewerVue from '@/components/Streaming/ViewerVue.vue';
import { fetchCourse } from "@/services/api/fetch";
import StudentPortalNavbar from '@/components/StudentPortal/StudentPortalNavbar.vue';

const props = defineProps<{ courseId: string }>();  
const emit = defineEmits(['closePortal']);  

const courseName = ref<string>('');
const isRecording = ref(false); 
const fakeNote = ref<string>(faker.lorem.paragraph(2)); 

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
 * Fetches and sets data for both the student and their courses.
 */
onMounted(async () => {
    loadCourseName(props.courseId);
});
</script>
    