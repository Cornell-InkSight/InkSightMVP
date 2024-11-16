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
            <div class="w-16 h-16 bg-gray-300 rounded-full mr-4"></div>
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
            <h3 class="text-lg font-semibold mb-2">Add Course</h3>

            <!-- Toggle Selection -->
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">Choose how to add a course:</label>
                <div class="flex items-center space-x-4">
                    <button 
                        @click="addExistingCourse = true" 
                        :class="['px-4 py-2 rounded-md', addExistingCourse ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700']">
                        Select Existing Course
                    </button>
                    <button 
                        @click="addExistingCourse = false" 
                        :class="['px-4 py-2 rounded-md', !addExistingCourse ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700']">
                        Add New Course
                    </button>
                </div>
            </div>

            <!-- Existing Course Dropdown -->
            <div v-if="addExistingCourse">
                <label for="existingCourse" class="block text-sm font-medium text-gray-700 mb-2">Select an Existing Course</label>
                <select 
                    v-model="selectedExistingCourseName" 
                    id="existingCourse" 
                    class="w-full px-4 py-2 border border-gray-300 rounded-md"
                >
                    <option value="" disabled>Select a course</option>
                    <option v-for="course in schoolCourses" :key="course.id" :value="course.name">
                        {{ course.name }}
                    </option>
                </select>
            </div>

            <!-- Add New Course Fields -->
            <div v-else>
                <label class="block text-sm font-medium text-gray-700 mb-2">Course Name</label>
                <input
                    v-model="newCourse.name"
                    type="text"
                    placeholder="Course Name"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
                />
            </div>

            <button 
                @click="submitCourse" 
                class="px-4 py-2 bg-blue-500 text-white rounded-md mt-4">
                Add Course
            </button>
            <p v-if="addCourseError" class="text-red-500 mt-2">{{ addCourseError }}</p>
        </div>

        <!-- Disability Section -->
        <p class="text-lg font-semibold mb-2">Disability:</p>
        <div class="flex items-center">
            <i class="fas fa-universal-access text-blue-500 mr-2"></i>
            <span>{{ student.disability }}</span>
        </div>
    </div>
</div>
</template>
    

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { fetchStudent, fetchCourses, fetchSchool, fetchSDSCoordinator, fetchCoursesForSchools } from '@/services/api/fetch';
import { addCourseForStudent } from "@/services/api/add"

const props = defineProps<{ id: number }>();
const emit = defineEmits(['closeProfile']);

const student = ref<any | null>(null);
const courses = ref<any[]>([]);
const loading = ref<boolean>(true);
const error = ref<string | null>(null);
const showAddCourseForm = ref(false); // Toggle between showing 
const addCourseError = ref<string | null>(null); // To Log error when adding course, if any
const school_id = ref(); // ID of the School
const sds_coordinator_id = ref(); // ID of the SDS Coordinator 
const addExistingCourse = ref(true); // Toggle between adding existing or new course
const selectedExistingCourseName = ref<string | null>(null); // For the dropdown
const schoolCourses = ref<any[]>([]); // Courses available for the school

// New course data
const newCourse = ref({
    name: '',
    school_id: school_id,
    sds_coordinator_id: sds_coordinator_id,
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
    if (!newCourse.value.name || !school_id || !sds_coordinator_id) {
        addCourseError.value = "All fields are required."; 
        return;
    }

    const { error: addError } = await addCourseForStudent(props.id, {
        name: newCourse.value.name,
        school_id: school_id.value,
        sds_coordinator_id: sds_coordinator_id.value
    });

    if (addError) {
        addCourseError.value = addError;
    } else {
        selectedExistingCourseName.value = "";
        addCourseError.value = null;
        showAddCourseForm.value = false;
        newCourse.value = { name: '', school_id: null, sds_coordinator_id: null };
        await loadStudentCourses();
    }
};

/**
 * Submit Course
 */
const submitCourse = async () => {
    if (addExistingCourse.value && selectedExistingCourseName.value) {
        await addCourseForStudent(props.id, { name: selectedExistingCourseName.value, school_id: school_id.value, sds_coordinator_id: sds_coordinator_id.value })
        selectedExistingCourseName.value = "";
        await loadSchoolCourses(school_id.value);
    } else if (!addExistingCourse.value && newCourse.value.name) {
        await addCourse();
    } else {
        addCourseError.value = "Please complete the required fields.";
    }
};

/**
 * Fetches the School data for the given School id and assigns to `schools`
 * Logs error message if request fails
 * @param sdscoordinatorId // the id of the given school from sdscoordinator-route params
 * @returns {Promise<void>} // A Promise that resolves when data is fetched and assigned
 */
 const loadSchool = async(schoolId: string) => {
    const { data, error: fetchError } = await fetchSchool(schoolId);
    if(fetchError) {
        console.error(fetchError)
        error.value = fetchError;
        return
    }
    school_id.value = data.id;
};

/**
 * Fetches the SDS Coordinator data for the given SDS Coordinator id and assigns to `sdscoordinator`
 * Logs error message if request fails
 * @param sdscoordinatorId // the id of the given SDS Coordinator from route params
 * @returns {Promise<void>} // A Promise that resolves when data is fetched and assigned
 */
 const loadSDSCoordinator = async (sdscoordinatorId: string) => {
    const { data, error } = await fetchSDSCoordinator(sdscoordinatorId);
    if (error) {
        console.error(error);
        return;
    }
    sds_coordinator_id.value = data.id;
};

/**
 * Fetches the courses for the respective school given ID.
 * @param schoolId - ID of the course
 */
 const loadSchoolCourses = async (schoolId: string) => {
    const { data, error: fetchError } = await fetchCoursesForSchools(schoolId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
    }
    await loadStudentCourses();
    schoolCourses.value = data
    schoolCourses.value = schoolCourses.value.filter(schoolCourse => !(courses.value.some(course => course.id === schoolCourse.id)))
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
    if(student) {
        await loadSchool(student.value.school_id);
        await loadSDSCoordinator(student.value.school_id);
        await loadSchoolCourses(student.value.school_id)
    }
    loading.value = false;
});
</script>
  