<template>
<div class="flex h-screen w-[15%] border-r-2 border-gray-100">
    <!-- Sidebar -->
    <aside class="w-full bg-gray-100 shadow-md flex flex-col">
    <!-- Header -->
    <div class="p-4 border-b">
        <button class="bg-blue-500 text-white text-sm px-4 py-2 rounded-lg w-full font-semibold">
        Professor Portal
        </button>
    </div>

    <!-- Navigation Links -->
    <nav class="flex-1 p-4">
        <ul class="space-y-2">
        <!-- Courses -->
        <li>
            <router-link
            :to="`/professors`"
            class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white font-bold"
            >
            <i class="fas fa-book-open mr-3 text-lg"></i>
            Courses
            </router-link>
        </li>

        <ul class="pl-8 mt-2 space-y-1 border-l-2 border-gray-300">
            <li v-for="course in courses" :key="course.id" class="flex items-center space-x-2">
            <!-- Bullet -->
            <span
                class="w-3 h-3 rounded-full"
                :class="(selectedProfessorCourseStore.selectedCourse && selectedProfessorCourseStore.selectedCourse.id==course.id) ? 'bg-purple-500' : 'bg-pink-300 opacity-50'"
            ></span>
            <!-- Course Name -->
            <button
                :class="(selectedProfessorCourseStore.selectedCourse && selectedProfessorCourseStore.selectedCourse.id==course.id) ? 'font-bold text-black' : 'text-gray-400 font-normal'"
                @click="selectedProfessorCourseStore.setCourse(course)"
            >
                {{ course.name.split(": ")[0] }}
            </button>
            </li>
        </ul>
        </ul>
    </nav>

    <!-- Footer Links -->
    <div class="p-4 border-t">
        <ul class="space-y-2">
        <!-- Settings -->
        <li>
            <router-link
            :to="`/sdscoordinators/settings`"
            class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white"
            >
            <i class="fas fa-cog mr-3 text-lg"></i>
            Settings
            </router-link>
        </li>

        <!-- Profile -->
        <li>
            <router-link
            :to="`/sdscoordinators/profile`"
            class="flex items-center text-gray-700 px-4 py-2 hover:bg-gray-200 hover:text-black rounded-lg transition-colors"
            active-class="bg-black text-white"
            >
            <i class="fas fa-user mr-3 text-lg"></i>
            Profile
            </router-link>
        </li>
        </ul>
    </div>
    </aside>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchCoursesForProfessors } from '@/services/api/fetch';
import { useUserStore } from "@/stores/authStore"
import { useSelectedProfessorCourseStore } from "@/stores/selectedProfessorCourseStore"
import * as interfaces from "@/services/api/interfaces";



const courses = ref<interfaces.Course[]>([]);
const selectedCourse = ref<interfaces.Course>();
// Loading Data For Selected Course for Interactive Navbar Component
const selectedProfessorCourseStore = useSelectedProfessorCourseStore();
/**
 * Fetches the courses for a specific professor
 */
 const loadCoursesForProfessor = async (professorId: string) => {
    const { data, error } = await fetchCoursesForProfessors(professorId);
    if (error) {
        console.error(error);
        return;
    }
    courses.value = data;
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their students.
 */
 onMounted(async () => {
    // Loading User Data
    const userStore = useUserStore()
    await userStore.fetchUser()
    const user = userStore.user;
    const professorId = user.user_ptr_id;
    await loadCoursesForProfessor(professorId);
});
</script>

<style scoped>
/* Sidebar Link Transitions */
aside a {
transition: color 0.3s ease, background-color 0.3s ease;
}

aside a.active {
background-color: #000; /* Active background */
color: #fff; /* Active text color */
}
</style>
      