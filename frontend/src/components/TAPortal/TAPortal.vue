<template>
<div class="flex min-h-screen bg-gray-100">
    <TAPortalNavbar />
    <div class="p-6 bg-gray-100 min-h-screen w-[80%]">
        <!-- Header with Title and Layout Options -->
        <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-bold text-gray-900">
            <span v-if="ta">{{ ta.name }}</span>
        </h1>
        <div class="flex items-center space-x-4">
            <!-- Search Bar -->
            <input 
            type="text" 
            placeholder="Search" 
            class="px-4 py-2 border border-gray-300 rounded-md focus:ring focus:border-blue-300"
            />
            <!-- Layout Icons -->
            <button class="p-2 rounded-md hover:bg-gray-200">
            <i class="fas fa-th-list"></i> <!-- List icon -->
            </button>
            <button class="p-2 rounded-md hover:bg-gray-200">
            <i class="fas fa-th"></i> <!-- Grid icon -->
            </button>
        </div>
        </div>
    
        <!-- Course Grid -->
        <div v-if="loading" class="text-center text-gray-500">
        <span class="animate-pulse">Loading courses...</span>
        </div>
        <div v-else-if="error" class="text-center text-red-500 font-semibold">
        {{ error }}
        </div>
        

        <!-- Course Details Modal -->
        <transition name="fade" mode="out-in">
        
            <TACourseView 
            v-if="selectedCourse" 
            :course="selectedCourse" 
            @closeModal="selectedCourse = null"
            />
            
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
            v-for="course in courses" 
            :key="course.id" 
            class="p-4 bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col justify-between items-stretch"
        >
            <!-- Course Header -->
            <div>
            <div class="flex">
                <h2 class="text-xl font-bold text-gray-900 mb-2 w-[100%]">{{ course.name.split(": ")[0] }}</h2>
                <button class="text-gray-500 hover:text-gray-700" @click="selectedCourse=course">
                <!-- Vertical Ellipsis Icon -->
                <i class="fas fa-info-circle"></i>
                </button>
            </div>
            <p class="text-sm text-gray-600">{{ course.name.split(": ")[1] }}</p>
            </div>
        </div>
        </div>
        </transition>
    </div>
</div>  
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { 
fetchTA, 
fetchProfessorsForCourses, 
fetchUnpublishedNotePacketsForCourse,
fetchCoursesForTA,  
} from "@/services/api/fetch";
import * as interfaces from "@/services/api/interfaces";
import TAPortalNavbar from '@/components/TAPortal/TAPortalNavbar.vue';
import { useUserStore } from "@/stores/authStore";
import TACourseView from '@/components/TAPortal/TACourseView.vue';

const route = useRoute(); 
const courses = ref<any[]>([]); // the list of courses the TA has
const ta = ref(null); // the object reference for the TA
const loading = ref<boolean>(true); // checks loading state
const error = ref<string | null>(null); // logs errors if any
const selectedCourse = ref<interfaces.Course>(); // The course selected for the modal


/**
 * Loads data for the TA from the API
 * @param taId - the ID of the TA
 */
const loadTA = async (taId: string) => {
    const { data, error: taError } = await fetchTA(taId);
    console.log(data)
    if (taError) {
        error.value = taError;
        return;
    } 
    ta.value = data;
};

/**
 * Loads the courses for respective TA, returns dictionary object with extra info needed for each course
 * Sets up Professors, top 5 most recent Notes packets
 * @param taId - ID of the TA 
 */
const loadCourses = async (taId: string) => {
    const { data, error: coursesError } = await fetchCoursesForTA(ta.value.user_ptr_id);
    if (coursesError) {
        error.value = coursesError;
    } else {
        const coursePromises = data.map(async (course: interfaces.Course) => {
        const professors = await loadProfessorsForCourses(course.id);
        const notesPackets = await loadNotesPacketsForCourse(parseInt(course.id));
        
        const recentNotesPackets = notesPackets.slice(0, 5).reverse();  

        return {
            ...course,
            professors,
            notesPackets: recentNotesPackets,
        };
        });
        courses.value = await Promise.all(coursePromises); 
    }
};

/**
 * Loads the professors for the course
 * @param courseId - ID of the course
 */
const loadProfessorsForCourses = async (courseId: string) => {
    const { data, error } = await fetchProfessorsForCourses(courseId);
    if (error) {
        console.error(error);
        return;
    }
    return data;
};

/**
 * Loads the note packets data for the respective course
 * @param courseId 
 */
const loadNotesPacketsForCourse = async (courseId: number) => {
    const { data, error } = await fetchUnpublishedNotePacketsForCourse(courseId.toString());
    console.log(data)
    if (error) {
        console.error(error);
        return [];
    }
    return data;
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for the TA and their courses and additional data.
 */
onMounted(async () => {
    const userStore = useUserStore()
    await userStore.fetchUser()
    const user = userStore.user;
    const taId = user.user_ptr_id;
    await loadTA(taId);
    await loadCourses(taId);
    loading.value = false; 
});
  </script>
  