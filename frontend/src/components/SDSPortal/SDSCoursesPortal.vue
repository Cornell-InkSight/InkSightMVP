<template>
<SDSPortalNavbar />
<div class="p-6 max-w-10xl mx-auto bg-gray-100 min-h-screen">
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

    <!-- Add Course Section -->
    <div class="mb-8">
        <button class="text-2xl font-bold mb-4" @click="toggleAddNewCourseModal">Add New Course</button>
        <form @submit.prevent="addNewCourse" v-if="addNewCourseModalIsOpen">
            <label for="courseName" class="block text-sm font-semibold text-gray-700">Course Name:</label>
            <input
                id="courseName"
                v-model="newCourseData.name"
                type="text"
                class="mt-2 w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter course name"
                required
            />
             <!-- Term -->
            <div>
                <label for="term" class="block text-sm font-semibold text-gray-700">Term</label>
                <input
                id="term"
                v-model="newCourseData.term"
                type="text"
                class="mt-2 w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter term (e.g., Fall 2024)"
                required
                />
            </div>

            <!-- Course UID -->
            <div>
                <label for="courseUID" class="block text-sm font-semibold text-gray-700">Course UID</label>
                <input
                id="courseUID"
                v-model="newCourseData.courseUID"
                type="number"
                class="mt-2 w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter unique course ID"
                required
                />
            </div>

            <!-- Type -->
            <div>
                <label for="type" class="block text-sm font-semibold text-gray-700">Type</label>
                <select
                id="type"
                v-model="newCourseData.type"
                class="mt-2 w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                required
                >
                <option value="" disabled>Select a type</option>
                <option value="Lecture">Lecture</option>
                <option value="Discussion">Discussion</option>
                </select>
            </div>

            <!-- Meeting Time -->
            <div>
                <label for="meetingTime" class="block text-sm font-semibold text-gray-700">Meeting Time</label>
                <input
                id="meetingTime"
                v-model="newCourseData.meetingTime"
                type="time"
                class="mt-2 w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                required
                />
            </div>

            <!-- Campus -->
            <div>
                <label for="campus" class="block text-sm font-semibold text-gray-700">Campus</label>
                <input
                id="campus"
                v-model="newCourseData.campus"
                type="text"
                class="mt-2 w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter campus location"
                required
                />
            </div>
            <button
                type="submit"
                class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md"
            >
                Add Course
            </button>
        </form>
    </div>

    <!-- Courses Section -->
    <div class="mb-4">
        <h2 class="text-2xl font-bold mb-4">Courses Offered</h2>

        <div v-if="courses && courses.length > 0" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-6">
        <div
            v-for="course in courses"
            :key="course.id"
            class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
        >
            <h3 class="text-lg font-bold text-gray-800">{{ course.name }}</h3>

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
                    <option v-for="professor in availableProfessors.filter(p => !course.professors.some(cp => p.user_ptr_id === cp.user_ptr_id))" :key="professor.user_ptr_id" :value="professor.user_ptr_id">
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
import { addNewProfessorCourse, addCourse } from "@/services/api/add";
import { useRoute } from 'vue-router';
import SDSPortalNavbar from "@/components/SDSPortal/SDSPortalNavbar.vue";
import * as interfaces from "@/services/api/interfaces"
import { useUserStore } from "@/stores/authStore";

const route = useRoute();
const courses = ref([]); // Holds courses for the school
const school = ref(); // Holds school
const sdscoordinator = ref(); // Holds SDS coordinator
const availableProfessors = ref([]); // Holds list of all available professors
const selectedProfessor = ref(null); // Holds selected professor ID from form
const error = ref<String>(); // Error message, if any exists
const loading = ref<boolean>(true); // Loading state indicator
const newCourseData = ref<interfaces.Course>({
  name: '', // Default empty name
  sds_coordinator_id: '', // Default SDS coordinator ID
  term: '', // Default term
  courseUID: 0, // Default unique course ID (e.g., 0 or any placeholder value)
  type: '', // Default type (e.g., 'Lecture' or 'Discussion')
  meetingTime: {} as TimeRanges, // Initialize meetingTime as an empty TimeRanges object
  campus: '', // Default campus name
});
const addNewCourseModalIsOpen = ref<boolean>(false); // Checks if the addNewCourseModal is open

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
    const { data, error: fetchError } = await fetchSDSCoordinator(sdscoordinatorId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
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

/**
 * Adds a new course for the school.
 */
 const addNewCourse = async () => {
    if (!newCourseData.value.name.trim()) {
        error.value = "Course name cannot be empty.";
        return;
    }

    const courseData = {
        name: newCourseData.value.name,
        school_id: sdscoordinator.value.school_id,
        sds_coordinator_id: sdscoordinator.value.user_ptr_id,
        term: newCourseData.value.term,
        courseUID: newCourseData.value.courseUID,
        type: newCourseData.value.type,
        meetingTime: newCourseData.value.meetingTime,
        campus: newCourseData.value.campus
    };

    try {
        const response = await addCourse(courseData);
        console.log("Course added:", response);

        // Reload courses after adding a new course
        await loadCoursesWithProfessors(sdscoordinator.value.school_id);

        // Clear the input field
        newCourseData.value = null;
    } catch (err) {
        console.error("Failed to add course:", err);
        error.value = "Failed to add course. Please try again.";
    }
};

/**
 * Toggles the Add New Course Modal
 */
const toggleAddNewCourseModal = () => {
    addNewCourseModalIsOpen.value = !addNewCourseModalIsOpen.value
}

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the courses and their professors and students.
 */
onMounted(async () => {
    const userStore = useUserStore()
    await userStore.fetchUser()
    const user = userStore.user;
    const sds_coordinator_id = user.user_ptr_id;
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
  