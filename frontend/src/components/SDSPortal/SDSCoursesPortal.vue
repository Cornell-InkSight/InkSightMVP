<template>
<SDSPortalNavbar />
<div class="p-6 max-w-6xl mx-auto bg-gray-100 min-h-screen">
    <!-- Error message -->
    <div v-if="error" class="text-red-500 font-semibold mb-4">
    {{ error }}
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center text-gray-500 animate-pulse">
    Loading data...
    </div>

    <!-- Content -->
    <div v-else>
    <!-- School and SDS Coordinator Information -->
    <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">School: {{ school?.name }}</h1>
        <p class="text-gray-700">SDS Coordinator: {{ sdscoordinator?.name }}</p>
    </div>

    <!-- Courses Section -->
    <div class="mb-4">
        <h2 class="text-2xl font-bold mb-4">Courses Offered</h2>

        <div v-if="courses && courses.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
            v-for="course in courses"
            :key="course.id"
            class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
        >
            <h3 class="text-lg font-bold text-gray-800">{{ course.name }}</h3>
            <p class="text-sm text-gray-600">Instructor: {{ course.instructor }}</p>
            <p class="text-sm text-gray-600">Credits: {{ course.credits }}</p>

            <!-- Professors List -->
            <div v-if="course.professors && course.professors.length > 0" class="mt-2">
            <h4 class="text-sm font-semibold text-gray-700">Professors:</h4>
            <ul class="mt-1 space-y-1">
                <li
                v-for="professor in course.professors"
                :key="professor.id"
                class="text-sm text-gray-600 bg-gray-100 rounded-md p-2"
                >
                {{ professor.name }}
                </li>
            </ul>
            </div>

            <!-- No Professors Message -->
            <p v-else class="text-sm text-gray-500">No professors assigned to this course.</p>

            <!-- Add Professor Form -->
            <form>
                <label for="professorSelect" class="block mt-4 text-sm font-semibold text-gray-700">Add a Professor:</label>
                <select
                    id="professorSelect"
                    v-model="course.selectedProfessor"
                    class="w-full mt-2 p-2 border border-gray-300 rounded-md"
                    required
                >
                    <option disabled value="">Select a professor</option>
                    <option v-for="professor in availableProfessors" :key="professor.id" :value="professor.id">
                    {{ professor.name }}
                    </option>
                </select>
                <button type="submit" @click="addNewProfessorToCourse(course.id, course.selectedProfessor)" class="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md">
                    Add Professor
            </button>
            </form>
        </div>
        </div>

        <!-- No Courses Message -->
        <div v-else class="text-gray-500">
        No courses available for this school.
        </div>
    </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchCoursesForSchools, fetchSDSCoordinator, fetchSchool, fetchProfessorsForCourses, fetchProfessorsForSchools } from "@/services/api/fetch";
import { addNewProfessorCourse } from "@/services/api/add";
import { useRoute } from 'vue-router';
import SDSPortalNavbar from "@/components/SDSPortal/SDSPortalNavbar.vue";

const route = useRoute();
const courses = ref([]); // Holds courses for the school
const school = ref(); // Holds school
const sdscoordinator = ref(); // Holds SDS coordinator
const availableProfessors = ref([]); // Holds list of all available professors
const selectedProfessor = ref(null); // Holds selected professor ID from form
const error = ref<String>(); // Error message, if any exists
const loading = ref<boolean>(true); // Loading state indicator

/**
 * Fetches all available professors.
 */
const loadAllProfessors = async (schoolId: string) => {
    const { data, error: fetchError } = await fetchProfessorsForSchools(schoolId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
    } else {
        availableProfessors.value = data;
    }
};

/**
 * Fetches the courses for the respective school given ID.
 */
const loadSchoolCourses = async (schoolId: string) => {
    const { data, error: fetchError } = await fetchCoursesForSchools(schoolId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
    }
    return data;
};

/**
 * Fetches the School data for the given School id.
 */
const loadSchool = async (schoolId: string) => {
    const { data, error: fetchError } = await fetchSchool(schoolId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
    }
    school.value = data;
};

/**
 * Fetches the SDS Coordinator data for the given SDS Coordinator id.
 */
const loadSDSCoordinator = async (sdscoordinatorId: string) => {
const { data, error } = await fetchSDSCoordinator(sdscoordinatorId);
if (error) {
    console.error(error);
    error.value = error;
}
sdscoordinator.value = data;
};

/**
 * Fetches professors for courses and loads them.
 */
const loadCoursesWithProfessors = async (school_id: string) => {
    let fetchedCourses = await loadSchoolCourses(school_id);
    if (!Array.isArray(fetchedCourses)) {
        console.error("Failed to fetch courses or invalid data format.");
        fetchedCourses = [];
    }

    const coursesWithProfessors = await Promise.all(
        fetchedCourses.map(async (course) => {
        const { data: professors, error } = await fetchProfessorsForCourses(course.id);
        const selectedProfessor = ref(null);
        return { ...course, professors, selectedProfessor };
    })
);

courses.value = coursesWithProfessors;
};

/**
 * Adds a new professor to a course.
 */
const addNewProfessorToCourse = async (course_id: string, professor_id: string) => {
    if (!professor_id) return;

    const professor_course_data = {
        course_id: course_id,
        professor_id: professor_id
    };

    try {
        const response = await addNewProfessorCourse(professor_course_data);
        console.log("Professor added:", response);

        // Reload the courses to show updated professor list
        await loadCoursesWithProfessors(school.value.id);
    } catch (error) {
        console.error("Failed to add professor to course:", error);
    }   
};

onMounted(async () => {
    const sds_coordinator_id = route.params.sdscoordinatorId as string;
    await loadSDSCoordinator(sds_coordinator_id);
    if (sdscoordinator.value) {
        const school_id = sdscoordinator.value.school_id;
        await loadSchool(school_id);
        await loadCoursesWithProfessors(school_id);
        await loadAllProfessors(school_id);
    }
    
    loading.value = false;
});
</script>
  