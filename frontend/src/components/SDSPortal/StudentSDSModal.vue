<template>
<div class="p-6 bg-white rounded-lg shadow-lg border border-gray-200">
    <button @click="$emit('closeProfile')" class="text-blue-500 mb-4">&larr; Back to all SDS students</button>
    <h2 class="text-2xl font-bold mb-4">Profile of {{ student?.name }}</h2>
    <div v-if="loading" class="text-center text-gray-500">
        <span class="animate-pulse">Loading student profile...</span>
    </div>
    <div v-else-if="error" class="text-center text-red-500 font-semibold">
        {{ error }}
    </div>
    <div v-else class="border p-4 rounded-lg bg-gray-50">
        <div class="flex items-center mb-4">
            <div class="w-16 h-16 bg-gray-300 rounded-full mr-4"></div> <!-- Placeholder for Profile Image -->
            <div>
                <h3 class="text-xl font-semibold">{{ student.name }}</h3>
            </div>
        </div>
        
        <!-- Courses Section -->
        <p class="text-lg font-semibold mb-2">Classes:</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
            <div 
            v-for="course in courses" 
            :key="course.id" 
            class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
            >
            <h4 class="text-md font-bold text-gray-800">{{ course.name }}</h4>
                <p class="text-sm text-gray-600">{{ course.description }}</p>
            </div>
        </div>
        
        <!-- Add Course Button -->
        <button @click="showAddCourseForm = !showAddCourseForm" class="text-blue-500 font-semibold mb-4">
            + Add New Course
        </button>

        <!-- Add Course Form -->
        <div v-if="showAddCourseForm" class="mb-4 border-t pt-4">
            <h3 class="text-lg font-semibold mb-2">Add New Course</h3>
            <input
            v-model="newCourse.name"
            type="text"
            placeholder="Course Name"
            class="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
            />
            <input
            v-model="newCourse.school_id"
            type="number"
            placeholder="School ID"
            class="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
            />
            <input
            v-model="newCourse.sds_coordinator_id"
            type="number"
            placeholder="SDS Coordinator ID"
            class="w-full px-4 py-2 border border-gray-300 rounded-md mb-4"
            />
            <button @click="addCourse" class="px-4 py-2 bg-blue-500 text-white rounded-md">
            Add Course
            </button>
            <p v-if="addCourseError" class="text-red-500 mt-2">{{ addCourseError }}</p>
        </div>
        
        <!-- Disability Section -->
        <p class="text-lg font-semibold mb-2">Disability:</p>
        <div class="flex items-center">
            <i class="fas fa-universal-access text-blue-500 mr-2"></i> <!-- Disability Icon -->
            <span>{{ student.disability }}</span>
        </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { fetchStudent, fetchCourses } from '@/services/api/fetch';
import { addCourseForStudent } from "@/services/api/add"

const props = defineProps<{ id: number }>();
const emit = defineEmits(['closeProfile']);

const student = ref<any | null>(null);
const courses = ref<any[]>([]);
const loading = ref<boolean>(true);
const error = ref<string | null>(null);
const showAddCourseForm = ref(false);
const addCourseError = ref<string | null>(null);

// New course data
const newCourse = ref({
    name: '',
    school_id: null,
    sds_coordinator_id: null,
});

/**
 * Fetches the student profile based on the provided id
 */
const loadStudentProfile = async () => {
    const { data, error: fetchError } = await fetchStudent(props.id);
    if (fetchError) {
        error.value = fetchError;
    } else {
        student.value = data;
    }
};

/**
 * Fetches the courses based on the student's id
 */
const loadStudentCourses = async () => {
    const { data, error: fetchError } = await fetchCourses(props.id);
    if (fetchError) {
        error.value = fetchError;
    } else {
        courses.value = data;
    }
};

/**
 * Adds a new course for the student by calling the API
 */
const addCourse = async () => {
    const { name, school_id, sds_coordinator_id } = newCourse.value;

    if (!name || !school_id || !sds_coordinator_id) {
        addCourseError.value = "All fields are required.";
        return;
    }

    const { error: addError } = await addCourseForStudent(props.id, {
        name,
        school_id,
        sds_coordinator_id
    });

    if (addError) {
        addCourseError.value = addError;
    } else {
        addCourseError.value = null;
        showAddCourseForm.value = false;
        newCourse.value = { name: '', school_id: null, sds_coordinator_id: null };
        await loadStudentCourses();
    }
};

/**
 * Watch for changes in `id` prop to reload profile if `id` changes.
 */
watch(() => props.id, async () => {
loading.value = true;
await loadStudentProfile();
await loadStudentCourses();
loading.value = false;
});

onMounted(async () => {
await loadStudentProfile();
await loadStudentCourses();
loading.value = false;
});
</script>
  