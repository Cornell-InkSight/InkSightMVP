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
            <p class="text-gray-700">Location: {{ school?.location }}</p>
            <p class="text-gray-700">SDS Coordinator: {{ sdscoordinator?.name }}</p>
        </div>
    
        <!-- professors Section -->
        <div class="mb-4">
            <h2 class="text-2xl font-bold mb-4">Professors in School</h2>
    
            <div v-if="professors && professors.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                <div
                    v-for="professor in professors"
                    :key="professor.id"
                    class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
                >
                    <h3 class="text-lg font-bold text-gray-800">{{ professor.name }}</h3>
                    <ul class="mt-2 space-y-1">
                        <li
                        v-for="course in professor.courses"
                        :key="course.id"
                        class="text-sm text-gray-600 bg-gray-100 rounded-md p-2"
                        >
                        {{ course.name }}
                        </li>
                    </ul>
                </div>
            </div>
    
            <!-- No professors Message -->
            <div v-else class="text-gray-500">
            No professors available for this school.
            </div>
        </div>
    </div>
</div>
</template>
    
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchProfessorsForSchools, fetchSDSCoordinator, fetchSchool, fetchCoursesForProfessors } from "@/services/api/fetch"
import { useRoute } from 'vue-router';
import SDSPortalNavbar from "@/components/SDSPortal/SDSPortalNavbar.vue"
    
const route = useRoute()
const professors = ref([]); // Holds professors for scohool
const school = ref() // Holds school
const sdscoordinator = ref() // Holds sds coordinator 
const error = ref<String>(); // Error message, if any exists
const loading = ref<boolean>(true)  // Loading state indicator

/**
 * Gets the professors for respective school given ID
 * Logs error if theres a request
 * 
 * @param schoolId // id of the given school to get professors
 * @returns {Promise<Void>} // Promise resolved when data is returned or error 
 */
const loadSchoolProfessors = async(schoolId: string) => {
    const { data, error: fetchError } = await fetchProfessorsForSchools(schoolId);
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
 * Fetches the Course Data for the given professor id, used in loop
 * Logs error, if the request fails
 */
const loadCoursesForProfessor = async (professorId: string) => {
    const { data, error } = await fetchCoursesForProfessors(professorId);
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
 const loadProfessorsWithCourses = async (school_id: string) => {
  let fetchedProfessors = await loadSchoolProfessors(school_id);
  if (!Array.isArray(fetchedProfessors)) {
    console.error("Failed to fetch professors or invalid data format.");
    fetchedProfessors = []; 
  }

  const professorsWithCourses = await Promise.all(
    fetchedProfessors.map(async (prof) => {
      const courses = await loadCoursesForProfessor(prof.id);
      return { ...prof, courses };
    })
  );

  professors.value = professorsWithCourses;
};




onMounted(async () => {
    let sds_coordinator_id = route.params.sdscoordinatorId as string;
    await loadSDSCoordinator(sds_coordinator_id);
    if(sdscoordinator) {
        let school_id = sdscoordinator.value.school_id;
        await loadSchool(school_id)
        await loadProfessorsWithCourses(school_id)
    }
    loading.value = false;
    
})


</script>
