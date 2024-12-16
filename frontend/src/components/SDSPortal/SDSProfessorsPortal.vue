<template>
<div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <SDSPortalNavbar />

    <!-- Main Content -->
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
            <div class ="mb-4 bg-gray-50 py-8 rounded-lg">
                <!-- School Information Header -->
                <div class="flex w-full">
                    <h2 class="text-2xl font-bold text-left pl-10 text-gray-900 mb-8 w-[83%]">Professors @ {{ school?.name }}</h2>
                    <button
                        @click="showAddProfessorModal = true"
                        class="bg-gray-900 h-[50%] text-white px-4 py-2 rounded-md hover:bg-gray-800 transition-all"
                    >
                        + Add New Professor
                    </button>
                </div>

            

                <!-- Professors Section -->
                <div class="mb-6 p-6">
                    <!-- Professors Grid -->
                    <div v-if="professors.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div
                        v-for="professor in professors"
                        :key="professor.user_ptr_id"
                        class="bg-white p-6 rounded-lg shadow-lg hover:shadow-2xl transition-all flex flex-col justify-between"
                    >
                        <h3 class="text-lg font-bold text-gray-900 mb-2">{{ professor.title || 'Professor' }} {{ professor.name }}</h3>

                        <!-- Courses List -->
                        <div class="mt-4 h-[70%]">
                            <h4 class="text-sm font-semibold text-gray-700 mb-2">Courses:</h4>
                            <ul class="space-y-1">
                                <li
                                v-for="course in professor.courses"
                                :key="course.id"
                                class="bg-gray-100 text-gray-700 rounded-md px-3 py-1 text-sm"
                                >
                                {{ course.name }}
                                </li>
                            </ul>
                        </div>

                        <!-- Add Existing Course Form -->
                        <div class="mt-4">
                        <label class="block text-sm font-medium text-gray-700 mb-1">Add Course</label>
                        <select
                            v-model="professor.selectedCourse"
                            class="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-black"
                        >
                            <option value="" disabled>Select a course</option>
                            <option
                            v-if="professor.courses"
                            v-for="course in availableCourses.filter(c => !professor.courses.some(cp => cp.id === c.id))"
                            :key="course.id"
                            :value="course.id"
                            >
                            {{ course.name }}
                            </option>
                        </select>
                        <button
                            @click="handleAddCourseToProfessor(professor.user_ptr_id, professor.selectedCourse)"
                            class="mt-2 w-full bg-black text-white py-2 rounded-md hover:bg-gray-800"
                        >
                            Add Course
                        </button>
                        </div>
                    </div>
                    </div>

                    <!-- No Professors Message -->
                    <div v-else class="text-gray-500 text-center py-6">
                    No professors available for this school.
                    </div>
                </div>

                <!-- Add Professor Modal -->
                <div
                    v-if="showAddProfessorModal"
                    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
                >
                    <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
                    <h2 class="text-2xl font-bold mb-4 text-gray-900">Add New Professor</h2>
                    <form @submit.prevent="handleAddProfessor">
                        <!-- Professor Name -->
                        <label class="block text-sm font-medium text-gray-700 mb-1">Professor Name</label>
                        <input
                        v-model="newProfessorName"
                        type="text"
                        class="w-full mb-4 px-4 py-2 border rounded-md focus:ring-2 focus:ring-black"
                        placeholder="Enter professor name"
                        />

                        <!-- Professor Email -->
                        <label class="block text-sm font-medium text-gray-700 mb-1">Professor Email</label>
                        <input
                        v-model="newProfessorEmail"
                        type="email"
                        class="w-full mb-4 px-4 py-2 border rounded-md focus:ring-2 focus:ring-black"
                        placeholder="Enter professor email"
                        />

                        <!-- Professor Title -->
                        <label class="block text-sm font-medium text-gray-700 mb-1">Professor Title</label>
                        <input
                        v-model="newProfessorTitle"
                        type="text"
                        class="w-full mb-4 px-4 py-2 border rounded-md focus:ring-2 focus:ring-black"
                        placeholder="e.g., Dr, Professor"
                        />

                        <!-- Modal Buttons -->
                        <div class="flex justify-end gap-2">
                        <button
                            @click="showAddProfessorModal = false"
                            type="button"
                            class="px-4 py-2 text-gray-700 rounded-md border border-gray-300 hover:bg-gray-200"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            class="px-4 py-2 bg-black text-white rounded-md hover:bg-gray-800"
                        >
                            Add Professor
                        </button>
                        </div>
                    </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
  
    
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchProfessorsForSchools, fetchSDSCoordinator, fetchSchool, fetchCoursesForProfessors, fetchCoursesForSchools} from "@/services/api/fetch"
import { useRoute } from 'vue-router';
import SDSPortalNavbar from "@/components/SDSPortal/SDSPortalNavbar.vue"
import { addProfessor, addNewProfessorCourse } from '@/services/api/add';
import { useUserStore } from "@/stores/authStore";

const route = useRoute()
const professors = ref([]); // Holds professors for scohool
const school = ref() // Holds school
const sdscoordinator = ref() // Holds sds coordinator 
const error = ref<String>(); // Error message, if any exists
const loading = ref<boolean>(true)  // Loading state indicator

const showAddProfessorModal = ref(false); // Controls visibility of the modal
const newProfessorName = ref(''); // Holds the name of the new professor
const newProfessorEmail = ref(''); // Holds the email of the new professor
const newProfessorTitle = ref(''); // Holds the title of the new professor

const availableCourses = ref([]); // List of all available courses
const selectedCourse = ref<string>(""); // Selected course for the dropdown

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
      const selectedProfessor = ref(null);
      let courses = await loadCoursesForProfessor(prof.user_ptr_id);
      if(!courses) {
        courses = []
      }
      return { ...prof, courses, selectedProfessor };
    })
  );

  professors.value = professorsWithCourses;
};

/**
 * Handles adding a new student.
 */
 const handleAddProfessor = async () => {
  if (!newProfessorName.value.trim()) {
    alert('Professor name is required.');
    return;
  }
  if (!newProfessorEmail.value.trim()) {
    alert('Professor email is required.');
    return;
  }
  if (!newProfessorTitle.value.trim()) {
    alert('Professor title is required.');
    return;
  }
  

  try {
    const newProfessor = {
      name: newProfessorName.value,
      email: newProfessorEmail.value,
      title: newProfessorTitle.value,
      school_id: sdscoordinator.value.school_id,
    };

    const addProfessors = await addProfessor(newProfessor);

    professors.value.push(addProfessors);
    loadAvailableCourses(sdscoordinator.value.school_id)

    newProfessorName.value = '';
    newProfessorEmail.value = '';
    newProfessorTitle.value = '';
    showAddProfessorModal.value = false;
  } catch (error) {
    console.error('Failed to add professor:', error);
    alert('Failed to add professor. Please try again.');
  }
};

/**
 * Fetches all available courses for the school.
 */
 const loadAvailableCourses = async (schoolId: string) => {
    const { data, error: fetchError } = await fetchCoursesForSchools(schoolId);
    if (fetchError) {
        console.error(fetchError);
        error.value = fetchError;
        return;
    }
    availableCourses.value = data || [];
};


/**
 * Handles adding a new course to a professor.
 */
 /**
 * Handles adding an existing course to a professor.
 */
const handleAddCourseToProfessor = async (professorId: string, course_id: string) => {
    if (!course_id) {
        alert('Please select a course.');
        return;
    }

    const courseData = {
        course_id: course_id,
        professor_id: professorId,
    };

    try {
        const response = await addNewProfessorCourse(courseData);
        console.log("Course added to professor:", response);

        // Reload professors and their courses
        await loadProfessorsWithCourses(school.value.id);

        selectedCourse.value = ''; // Clear the dropdown
    } catch (err) {
        console.error("Failed to add course to professor:", err);
        alert("Failed to add course. Please try again.");
    }
};


/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their SDS coordinaotrs.
 */
onMounted(async () => {
    const userStore = useUserStore()
    await userStore.fetchUser()
    const user = userStore.user;
    const sds_coordinator_id = user.user_ptr_id;
    await loadSDSCoordinator(sds_coordinator_id);
    if(sdscoordinator) {
        let school_id = sdscoordinator.value.school_id;
        await loadSchool(school_id)
        await loadProfessorsWithCourses(school_id)
        await loadAvailableCourses(school_id)
    }
    loading.value = false;
    
})


</script>
