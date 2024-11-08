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
import { ref, onMounted } from 'vue'
import { fetchCoursesForSchools, fetchSDSCoordinator, fetchSchool, fetchProfessorsForCourses } from "@/services/api/fetch"
import { useRoute } from 'vue-router';
import SDSPortalNavbar from "@/components/SDSPortal/SDSPortalNavbar.vue"

const route = useRoute()
const courses = ref([]); // Holds courses for scohool
const school = ref() // Holds school
const sdscoordinator = ref() // Holds sds coordinator 
const error = ref<String>(); // Error message, if any exists
const loading = ref<boolean>(true)  // Loading state indicator

/**
 * Gets the courses for respective school given ID
 * Logs error if theres a request
 * 
 * @param schoolId // id of the given school to get courses
 * @returns {Promise<Void>} // Promise resolved when data is returned or error 
 */
const loadSchoolCourses = async(schoolId: string) => {
    const { data, error: fetchError } = await fetchCoursesForSchools(schoolId);
    if(fetchError) {
        console.error(fetchError)
        error.value = fetchError;
        return
    }
    return data;
}

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
    school.value = data;
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
    sdscoordinator.value = data;
};


/**
 * Fetches the Professors Data for the given course id, used in loop
 * Logs error, if the request fails
 */
 const loadProfessorsForCourses = async (professorId: string) => {
    const { data, error } = await fetchProfessorsForCourses(professorId);
    if(error) {
        console.error(error);
        return;
    }
    return data;
}


/**
 * Fetches professors and loads their courses.
 * Logs error, if the request fails
 * @param school_id // the id of the school for requesting the professors
 */
 const loadCoursesWithProfessors = async (school_id: string) => {
  let fetchedCourses = await loadSchoolCourses(school_id);
  if (!Array.isArray(fetchedCourses)) {
    console.error("Failed to fetch professors or invalid data format.");
    fetchedCourses = []; 
  }

  const loadCoursesWithProfessors = await Promise.all(
    fetchedCourses.map(async (course) => {
      const professors = await loadProfessorsForCourses(course.id);
      return { ...course, professors };
    })
  );

  courses.value = loadCoursesWithProfessors;
};

onMounted(async () => {
    let sds_coordinator_id = route.params.sdscoordinatorId as string;
    await loadSDSCoordinator(sds_coordinator_id);
    if(sdscoordinator) {
        let school_id = sdscoordinator.value.school;
        await loadSchool(school_id)
        await loadCoursesWithProfessors(school_id)
    }
    loading.value = false;
    
})


</script>
