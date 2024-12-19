<template>
<!-- Course Details -->
<div class="space-y-6">    
    <!-- Course Information -->
    <div class="border border-gray-300 bg-white p-4 rounded-lg">
    <h3 class="text-lg font-bold text-gray-900 mb-4">Course Information</h3>
    <ul class="text-sm text-gray-700 space-y-2">
        <li><strong class="text-gray-900">Term:</strong> {{ selectedProfessorCourseStore.selectedCourse.term }}</li>
        <li><strong class="text-gray-900">Course ID:</strong> {{ selectedProfessorCourseStore.selectedCourse.course_uid }}</li>
        <li><strong class="text-gray-900">Type:</strong> {{ selectedProfessorCourseStore.selectedCourse.type }}</li>
        <li><strong class="text-gray-900">Campus:</strong> {{ selectedProfessorCourseStore.selectedCourse.campus }}</li>
        <li>
        <strong class="text-gray-900">Meeting Times:</strong>
        <div class="text-gray-700 space-y-1">
            <p>{{ selectedProfessorCourseStore.selectedCourse.meeting_time }}</p>
        </div>
        </li>
        <!-- TA Section -->
        <div v-if="tas && tas.length > 0" class="mt-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700">TAs:</h4>
            <ul class="mt-1 space-y-1">
            <li v-for="ta in tas" :key="ta.user_ptr_id" class="text-sm text-gray-600 bg-gray-100 rounded-md p-2">
                {{ ta.name }}
            </li>
            </ul>
        </div>
    </ul>
    </div>
</div>
</template>

<script setup lang="ts">
import { fetchTAsForCourse } from '@/services/api/fetch';
import { ref, onMounted } from 'vue';
import * as interfaces from "@/services/api/interfaces";
import { useUserStore } from "@/stores/authStore";
import { da } from '@faker-js/faker/.';
import { useSelectedProfessorCourseStore } from "@/stores/selectedProfessorCourseStore"


const selectedProfessorCourseStore = useSelectedProfessorCourseStore();

const tas = ref<interfaces.TA[]>(); // TAs for course
const error = ref<string>();

/**
 * Fetches data for a specific professor by ID and assigns it to `professor`.
 */
const loadTAs = async (professorId: string, courseId: string): Promise<void> => {
    const { data, error: fetchError } = await fetchTAsForCourse(professorId, courseId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
        return;
    }
    tas.value = data;
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the data.
 */
onMounted(async () => {
    const userStore = useUserStore()
    await userStore.fetchUser()
    const user = userStore.user;
    const professorId = user.user_ptr_id;
    await loadTAs(professorId, selectedProfessorCourseStore.selectedCourse.id)
});
</script>

<style scoped>
ul li {
line-height: 1.6; 
}
</style>
    