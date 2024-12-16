<template>
<div class="flex min-h-screen bg-gray-100">
  <SDSPortalNavbar />
  <div class="p-6 bg-gray-100 min-h-screen w-[80%]">
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
        <!-- Add Course Section -->
        <div v-if="addNewCourseModalIsOpen" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50">
            <div class="bg-white rounded-lg shadow-lg w-full max-w-3xl">
                <!-- Modal Header -->
                <div class="flex justify-between items-center p-4 border-b border-gray-200">
                <h2 class="text-2xl font-semibold text-gray-800">Add New Course</h2>
                <button @click="toggleAddNewCourseModal" class="text-gray-600 hover:text-gray-900">
                    &times;
                </button>
                </div>

                <!-- Modal Body -->
                <div class="p-6 space-y-4">
                <!-- Course Name -->
                <div>
                    <label for="courseName" class="block text-sm font-medium text-gray-700 mb-1">Course Name</label>
                    <input
                    id="courseName"
                    v-model="newCourseData.name"
                    type="text"
                    placeholder="Enter course name"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:outline-none"
                    />
                </div>

                <!-- Term -->
                <div>
                    <label for="term" class="block text-sm font-medium text-gray-700 mb-1">Term</label>
                    <input
                    id="term"
                    v-model="newCourseData.term"
                    type="text"
                    placeholder="Enter term (e.g., Fall 2024)"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:outline-none"
                    />
                </div>

                <!-- Type Dropdown -->
                <div>
                    <label for="type" class="block text-sm font-medium text-gray-700 mb-1">Type</label>
                    <select
                    id="type"
                    v-model="newCourseData.type"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:outline-none"
                    >
                    <option value="" disabled>Select type</option>
                    <option value="Lecture">Lecture</option>
                    <option value="Discussion">Discussion</option>
                    </select>
                </div>

                <!-- Course UID -->
                <div>
                    <label for="courseUID" class="block text-sm font-medium text-gray-700 mb-1">Course UID</label>
                    <input
                    id="courseUID"
                    v-model="newCourseData.courseUID"
                    type="number"
                    placeholder="Enter unique course UID"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:outline-none"
                    />
                </div>

                <!-- Meeting Time -->
                <div>
                    <label for="meetingTime" class="block text-sm font-medium text-gray-700 mb-1">Meeting Time</label>
                    <input
                    id="meetingTime"
                    v-model="newCourseData.meetingTime"
                    type="time"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:outline-none"
                    />
                </div>

                <!-- Campus -->
                <div>
                    <label for="campus" class="block text-sm font-medium text-gray-700 mb-1">Campus</label>
                    <input
                    id="campus"
                    v-model="newCourseData.campus"
                    type="text"
                    placeholder="Enter campus location"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:outline-none"
                    />
                </div>
                </div>

                <!-- Modal Footer -->
                <div class="flex justify-end items-center p-4 border-t border-gray-200">
                <button
                    @click="toggleAddNewCourseModal"
                    class="text-gray-600 px-4 py-2 mr-2 hover:text-gray-800"
                >
                    Cancel
                </button>
                <button
                    @click="addNewCourse"
                    class="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-800 transition"
                >
                    Add Course
                </button>
                </div>
            </div>
        </div>


        <!-- Courses Section -->
        <div class="mb-4 bg-gray-50 py-8 rounded-lg">
            <div class="flex w-full">
                <h2 class="text-2xl font-bold text-left pl-10 text-gray-900 mb-8 w-[83%]">Courses Offered @ {{ school?.name }}</h2>
                <button
                    @click="toggleAddNewCourseModal"
                    class="bg-gray-900 h-[50%] text-white px-4 py-2 rounded-md hover:bg-gray-800 transition-all"
                >
                    + Add New Course
                </button>
            </div>
            <div v-if="courses && courses.length > 0" class="p-4  grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-3 gap-6 w-full">
                <div v-for="course in courses" :key="course.id" class="p-6 bg-white rounded-xl shadow-lg border border-gray-100 hover:shadow-2xl transition-all duration-30 flex flex-col justify-between items-stretch">
                    <div class="min-h-[10%] mb-8">
                        <h3 class="text-xl font-bold text-gray-900 w-[100%]">{{ course.name.split(": ")[0] }}</h3>
                        <p class="text-sm text-gray-600">{{ course.name.split(": ")[1] }}</p>
                    </div>
                    <div class="min-h-[10%] mb-8 grid grid-cols-1 gap-y-1 mb-3 text-sm text-gray-700 min-h-6">
                        <div class="font-semibold">Term: {{ course.term || 'N/A' }}</div>

                        <div class="font-semibold">Type: {{ course.type || 'N/A' }}</div>
                    </div>


                    <!-- Professors Section -->
                    <div class="h-[40%] mb-2">
                        <h4 class="text-sm font-semibold text-gray-700 mb-2">Professors:</h4>
                        <ul>
                        <li
                            v-for="professor in course.professors"
                            :key="professor.id"
                            class="text-sm text-gray-600 bg-gray-100 rounded-md p-2 mb-1"
                        >
                            {{ professor.name }}
                        </li>
                        </ul>
                    </div>

                    <!-- Add Professor Dropdown -->
                    <div class="mt-4">
                        <label class="block text-sm font-medium text-gray-700">Add a Professor</label>
                        <select
                        v-model="course.selectedProfessor"
                        class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900"
                        >
                        <option value="" disabled>Select a professor</option>
                        <option
                            v-for="professor in availableProfessors.filter(p => !course.professors.some(cp => cp.id === p.id))"
                            :key="professor.id"
                            :value="professor.id"
                        >
                            {{ professor.name }}
                        </option>
                        </select>
                        <button
                        @click="addNewProfessorToCourse(course.id, course.selectedProfessor)"
                        class="mt-2 w-full bg-gray-900 text-white py-2 rounded-md hover:bg-gray-800"
                        >
                        Add Professor
                        </button>
                    </div>
                </div>
            </div>

            <!-- No Courses Message -->
            <div v-else class="text-gray-500">
                No courses available for this school.
            </div>
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
  