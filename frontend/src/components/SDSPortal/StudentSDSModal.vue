<template>
<div class="p-6 bg-gray-50 min-h-screen">
    <!-- Back Button -->
    <button 
    @click="$emit('closeProfile')" 
    class="text-blue-600 text-sm font-medium hover:underline mb-4 block"
    >
    &larr; Back to all SDS students
    </button>

    <!-- Profile Header -->
    <h2 class="text-3xl font-bold mb-6">{{ student?.name }}</h2>

    <!-- Main Content -->
    <div class="bg-white rounded-lg shadow-md border border-gray-200">
        <div class="grid grid-cols-1 lg:grid-cols-2">
            <!-- Left Column - Request Details -->
            <div class="p-6 border-r border-gray-200">
                <h3 class="font-bold text-lg mb-2">Request details</h3>
                <p class="text-sm text-gray-700">
                    <span class="font-semibold block mb-2">Accommodation request:</span>
                    {{ student?.accodomation_request }}
                </p>
            </div>

            <!-- Right Column - Enabled Features -->
            <div class="p-6">
                <h3 class="font-bold text-lg mb-4">Enabled features:</h3>
                <div class="flex flex-wrap items-center gap-3">
                    <!-- Feature Buttons -->
                    <button 
                    v-for="feature in features" 
                    :key="feature.name" 
                    class="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-300 shadow-sm text-gray-700"
                    >
                    <i :class="feature.icon"></i> {{ feature.name }}
                    </button>
                </div>

                <!-- Enable New Feature Button -->
                <div class="mt-6">
                    <button 
                    @click="openFeatureModal" 
                    class="w-full bg-black text-white py-2 rounded-lg flex items-center justify-center gap-2 hover:bg-gray-800"
                    >
                    <span>+ Enable new feature</span>
                    </button>
                </div>

                <!-- Feature Selection Modal -->
                <div v-if="showFeatureModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg shadow-lg w-[400px]">
                        <!-- Modal Header -->
                        <div class="p-4 border-b border-gray-200">
                        <h3 class="text-lg font-bold text-gray-900">Enable New Features</h3>
                        </div>

                        <!-- Feature List -->
                        <div class="p-4 max-h-[300px] overflow-y-auto">
                        <div
                            v-for="feature in features"
                            :key="feature.name"
                            class="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-gray-50"
                        >
                            <div class="flex items-center gap-2">
                            <input 
                                type="checkbox" 
                                :id="feature.name" 
                                v-model="enabledFeatures" 
                                :value="feature"
                                class="w-5 h-5 text-gray-800 border-gray-300 rounded focus:ring-2 focus:ring-black"
                            />
                            <label :for="feature.name" class="flex items-center gap-2 text-gray-700 cursor-pointer">
                                <i :class="feature.icon" class="text-gray-600"></i>
                                <span>{{ feature.name }}</span>
                            </label>
                            </div>
                        </div>
                        </div>

                    <!-- Modal Footer -->
                    <div class="p-4 border-t border-gray-200 flex justify-end gap-2">
                        <button 
                            @click="closeFeatureModal" 
                            class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300">
                            Cancel
                        </button>
                        <button 
                            @click="submitFeatures" 
                            class="px-4 py-2 text-white bg-black rounded-lg hover:bg-gray-800">
                            Save Features
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Classes Section -->
<div class="mt-8 bg-white rounded-lg shadow-md border border-gray-200">
    <div class="p-6">
        <h3 class="text-lg font-bold mb-4">Classes:</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        <div 
            v-for="course in courses" 
            :key="course.id" 
            class="p-4 bg-gray-100 rounded-lg shadow-sm border border-gray-300"
        >
            <h4 class="font-bold">{{ course.name }}</h4>
            <p class="text-sm text-gray-500">{{ course.description }}</p>
        </div>
        </div>

        <!-- Add Course Button -->
        <button 
        @click="showAddCourseForm = !showAddCourseForm" 
        class="text-blue-600 font-medium hover:underline"
        >
        + Add New Course
        </button>

        <!-- Add Course Form -->
        <div v-if="showAddCourseForm" class="mt-6 border-t border-gray-200 pt-6">
            <!-- Section Header -->
            <h3 class="text-xl font-semibold mb-4 text-gray-900">Add Course</h3>

            <!-- Existing Course Dropdown -->
            <div v-if="addExistingCourse" class="mb-4">
                <!-- <label for="existingCourse" class="block text-sm font-medium text-gray-700 mb-2">
                Select Course
                </label> -->
                <select
                v-model="selectedExistingCourseName"
                id="existingCourse"
                class="w-[75%] px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-gray-900 focus:outline-none"
                >
                <option value="" disabled>Select a course</option>
                <option v-for="course in schoolCourses" :key="course.id" :value="course.id">
                    {{ course.name }}
                </option>
                </select>
            </div>

            <!-- Add New Course Fields -->
            <div v-else class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">Course Name</label>
                <input
                v-model="newCourse.name"
                type="text"
                placeholder="Course Name"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-gray-900 focus:outline-none"
                />
            </div>

            <!-- Submit Course Button -->
            <button
                @click="submitCourse"
                class="w-40 bg-black text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition-all"
            >
                Add Course
            </button>

            <!-- Error Message -->
            <p v-if="addCourseError" class="text-red-600 text-sm mt-2">{{ addCourseError }}</p>
            </div>

    </div>
    </div>
</div>
</template>
  

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { fetchStudent, fetchCourses, fetchSchool, fetchSDSCoordinator, fetchCoursesForSchools, fetchNoteTakingRequestStudentForCourse } from '@/services/api/fetch';
import { addNewCourseForStudent, addStudentToCourse } from "@/services/api/add"

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
const showFeatureModal = ref<boolean>();

const features = [{name: "Diction", icon: "fas fa-microphone"}, {name: "Visual", icon: "fas fa-sketch"}]

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
    const { data, error: fetchError } = await fetchStudent(props.id.toString());
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
    const { data, error: fetchError } = await fetchCourses(props.id.toString());
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

    const { error: addError } = await addNewCourseForStudent(props.id, {
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
    // if (addExistingCourse.value && selectedExistingCourseName.value) {
    //     await addNewCourseForStudent(props.id, { name: selectedExistingCourseName.value, school_id: school_id.value, sds_coordinator_id: sds_coordinator_id.value })
    //     selectedExistingCourseName.value = "";
    //     await loadSchoolCourses(school_id.value);
    // } else if (!addExistingCourse.value && newCourse.value.name) {
    //     await addCourse();
    // } else {
    //     addCourseError.value = "Please complete the required fields.";
    // }
    if(addExistingCourse.value) {
        addStudentToCourse(student.value.user_ptr_id, parseInt(selectedExistingCourseName.value))
        selectedExistingCourseName.value = "";
        await loadStudentCourses();
        await loadSchoolCourses(school_id.value);
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
    sds_coordinator_id.value = data.user_ptr_id;
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
 * Feature Functions
 */
const enabledFeatures = ref([]);

// Function to open modal
const openFeatureModal = () => {
  showFeatureModal.value = true;
};

// Function to close modal
const closeFeatureModal = () => {
  showFeatureModal.value = false;
};

const submitFeatures = () => {

}


/**
 * Watch for changes in `id` prop to reload profile if `id` changes.
 */
watch(() => props.id, async () => {
    loading.value = true;
    await loadStudentProfile();
    await loadStudentCourses();
    loading.value = false;
});

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for student profile
 */
onMounted(async () => {
    await loadStudentProfile();
    await loadStudentCourses();
    if(student) {
        await loadSchool(student.value.school_id);
        await loadSDSCoordinator(student.value.sds_coordinator_id);
        await loadSchoolCourses(student.value.school_id)
    }
    loading.value = false;
});
</script>

