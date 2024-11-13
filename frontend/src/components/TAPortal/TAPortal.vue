<template>
<TAPortalNavbar />
<div class="max-w-6xl mx-auto p-6 bg-gray-100 min-h-screen">
    <!-- Header with Title and Layout Options -->
    <div class="flex items-center justify-between mb-6">
    <h1 class="text-3xl font-bold text-gray-900">
        Classes for <span v-if="ta">{{ ta.name }}</span>
    </h1>
    <div class="flex items-center space-x-4">
        <!-- Search Bar -->
        <input 
        type="text" 
        placeholder="Search" 
        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300"
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
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div 
        v-for="course in courses" 
        :key="course.id" 
        class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
    >
        <h2 class="text-xl font-bold text-gray-800">{{ course.name }}</h2>

        <!-- Approval Check -->
        <div>
            <!-- Professors Section -->
            <div v-if="course.professors && course.professors.length > 0" class="mt-2">
                <h4 class="text-sm font-semibold text-gray-700">Professors:</h4>
                <ul class="mt-1 space-y-1">
                <li v-for="professor in course.professors" :key="professor.id" class="text-sm text-gray-600 bg-gray-100 rounded-md p-2">
                    {{ professor.name }}
                </li>
                </ul>
            </div>

            <!-- Most Recent Notes Packets -->
            <div v-if="course.notesPackets && course.notesPackets.length > 0" class="mt-4">
                <h4 class="text-sm font-semibold text-gray-700">Recent Notes Packets:</h4>
                <ul class="mt-1 space-y-1">
                <li 
                    v-for="packet in course.notesPackets" 
                    :key="packet.id" 
                    class="text-sm text-gray-500 bg-gray-50 rounded-md p-2 hover:bg-gray-100"
                >
                    <div class="text-blue-500 hover:underline">
                    <router-link :to="`/notepackets/${packet.id}/edit`" target='_blank'>
                        Packet from Lecture Session {{ packet.lecture_session_id }}
                    </router-link>
                    </div>
                </li>
                </ul>
            </div>
            <p v-else class="text-sm text-gray-500">No recent notes packets available.</p>
        </div>
    </div>
    </div>
</div>  
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { 
fetchTA, 
fetchCourses, 
fetchProfessorsForCourses, 
fetchUnpublishedNotePacketsForCourse,  
} from "@/services/api/fetch";
import * as interfaces from "@/services/api/interfaces";
import TAPortalNavbar from '@/components/TAPortal/TAPortalNavbar.vue';

const route = useRoute();
const courses = ref<any[]>([]);
const ta = ref(null);
const loading = ref<boolean>(true);
const error = ref<string | null>(null);

const loadTA = async (taId: string) => {
const { data, error: taError } = await fetchTA(taId);
if (taError) {
    error.value = taError;
    return;
} 
ta.value = data;
};

const loadCourses = async (taId: string) => {
const { data, error: coursesError } = await fetchCourses(taId);
if (coursesError) {
    error.value = coursesError;
} else {
    const coursePromises = data.map(async (course: interfaces.Course) => {
    const professors = await loadProfessorsForCourses(course.id);
    const notesPackets = await loadNotesPacketsForCourse(course.id);
    
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

const loadProfessorsForCourses = async (courseId: string) => {
const { data, error } = await fetchProfessorsForCourses(courseId);
if (error) {
    console.error(error);
    return;
}
return data;
};

const loadNotesPacketsForCourse = async (courseId: number) => {
    const { data, error } = await fetchUnpublishedNotePacketsForCourse(courseId);
    console.log(data)
    if (error) {
        console.error(error);
        return [];
    }
    return data;
};

onMounted(async () => {
const taId = route.params.taId as string;
await loadTA(taId);
await loadCourses(taId);
loading.value = false; 
});
  </script>
  