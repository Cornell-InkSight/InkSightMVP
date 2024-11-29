<template>
<SDSPortalNavbar />
<div class="max-w-6xl mx-auto p-6 bg-gray-100 min-h-screen">
  <!-- Header with Title and Layout Options -->
  <div class="flex items-center justify-between mb-6">
    <h1 class="text-3xl font-bold text-gray-900">
      Students under jurisdiction of
      <span v-if="sdscoordinator">{{ sdscoordinator.name }} at {{ school?.name }}</span>
    </h1>
    <div class="flex items-center space-x-4">
      <!-- Search Bar -->
      <input 
        type="text" 
        placeholder="Search" 
        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300"
      />
      <!-- Layout Icons -->
      <button class="p-2 rounded-md hover:bg-gray-200">
        <i class="fas fa-th-list"></i> <!-- List icon -->
      </button>
      <button class="p-2 rounded-md hover:bg-gray-200">
        <i class="fas fa-th"></i> <!-- Grid icon -->
      </button>
    </div>
  </div>

  <!-- Add New Student Button -->
  <div class="mb-6" v-if="!selectedStudentId" >
    <button 
      @click="showAddStudentModal = true" 
      class="px-4 py-2 bg-blue-500 text-white rounded-md shadow hover:bg-blue-600"
    >
      + Add New Student
    </button>
  </div>

  <!-- Add Student Modal -->
  <div 
    v-if="showAddStudentModal" 
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
      <h2 class="text-xl font-bold mb-4">Add New Student</h2>
      <form @submit.prevent="handleAddStudent">
        <label class="block mb-2">
          <input 
            v-model="newStudentName" 
            type="text" 
            class="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
            placeholder="Enter student name"
          />
          <input 
            v-model="newStudentEmail" 
            type="text" 
            class="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
            placeholder="Enter student email"
          />
          <input 
            v-model="newStudentDisability" 
            type="text" 
            class="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
            placeholder="Enter student disability"
          />
          <input 
            v-model="newStudentYear" 
            type="text" 
            class="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
            placeholder="Enter student year"
          />
        </label>
        <div class="flex items-center justify-end mt-4">
          <button 
            @click="showAddStudentModal = false" 
            type="button" 
            class="px-4 py-2 bg-gray-500 text-white rounded-md shadow hover:bg-gray-600 mr-2"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            class="px-4 py-2 bg-blue-500 text-white rounded-md shadow hover:bg-blue-600"
          >
            Add Student
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Transition for Profile View -->
  <transition name="fade" mode="out-in">
    <StudentSDSModal 
      v-if="selectedStudentId" 
      :id="selectedStudentId" 
      @closeProfile="selectedStudentId = null" 
      key="profile-view" 
    />
    
    <!-- Student Grid -->
    <div v-else key="grid-view" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <button 
        v-for="student in students" 
        :key="student.id" 
        class="p-4 bg-white rounded-lg shadow-md border border-gray-200"
        @click="selectedStudentId = student.user_ptr_id"
      >
        <h2 class="text-xl font-bold text-gray-800">{{ student.name }}</h2>
        <p class="text-gray-600">{{ student.disability }}</p>
      </button>
    </div>
  </transition>
</div>
</template>

  
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchStudentsForSDSCoordinators, fetchSDSCoordinator, fetchSchool } from '@/services/api/fetch';
import { addStudent } from '@/services/api/add';
import { useRoute } from 'vue-router'
import StudentSDSModal from '@/components/SDSPortal/StudentSDSModal.vue';
import SDSPortalNavbar from "@/components/SDSPortal/SDSPortalNavbar.vue"

const route = useRoute()
const sdscoordinator = ref<any | null>(null); // Holds SDS Coordinator data, initially null
const students = ref<any[]>([]) // Holds list of students associated with SDS Coordinator
const school = ref<any | null>(null); // Holds SDS Coordinator's School data, initially null
const loading = ref<boolean>(true); // Loading State indicator
const error = ref<string | null>(null); // Error message
const selectedStudentId = ref<number | null>(null) // Holds selected student id

const showAddStudentModal = ref(false); // Controls visibility of the modal
const newStudentName = ref(''); // Holds the name of the new student
const newStudentEmail = ref(''); // Holds the name of the new student
const newStudentDisability = ref(''); // Holds the disability of the new student
const newStudentYear = ref(''); // Holds the year of the new student

/**
 * Fetches the students for the specific SDS Coordinator and assigns them to `students`
 * Logs an error message if request fails
 * @param sdscoordinatorId // the id of the given SDS Coordinator from route params
 * @returns {Promise<void>} // A Promise that resolves when the data is fetched and assigned.
 */
const loadStudents = async (sdscoordinatorId: string) => {
    const { data, error } = await fetchStudentsForSDSCoordinators(sdscoordinatorId);
    if (error) {
        console.error(error);
        return;
    }
    students.value = data;
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
 * Fetches the school from the given School id and assigns to `school`
 * logs error message if request fails
 * @param schoolId // the id of the given School from the SDS Cooordinator
 * @returns {Promise<void>} // A promise that resolves when the data is fetched and assigned
 */
const loadSchool = async (schoolId: string) => {
    const { data, error } = await fetchSchool(schoolId);
    console.log(data)
    if (error) {
        console.error(error);
        return;
    }
    school.value = data;
};

/**
 * Handles adding a new student.
 */
 const handleAddStudent = async () => {
  if (!newStudentName.value.trim()) {
    alert('Student name is required.');
    return;
  }
  if (!newStudentEmail.value.trim()) {
    alert('Student email is required.');
    return;
  }
  if (!newStudentDisability.value.trim()) {
    alert('Student disability is required.');
    return;
  }
  

  try {
    const newStudent = {
      name: newStudentName.value,
      email: newStudentEmail.value,
      sds_coordinator_id: sdscoordinator.value?.user_ptr_id,
      school_id: sdscoordinator.value.school_id,
      disability: newStudentDisability.value,
      year: newStudentYear.value,
    };

    const addedStudent = await addStudent(newStudent);

    students.value.push(addedStudent);

    newStudentName.value = '';
    newStudentDisability.value = '';
    newStudentYear.value = '';
    showAddStudentModal.value = false;
  } catch (error) {
    console.error('Failed to add student:', error);
    alert('Failed to add student. Please try again.');
  }
};



/**
 * Lifecycle hook called when component is mounted.
 * Fecthes and sets data for both SDS Coordinator and their students
 */
onMounted(async () => {
    const sdscoordinatorId = route.params.sdscoordinatorId as string;
    await loadSDSCoordinator(sdscoordinatorId);
    if (sdscoordinator.value) {
        await loadSchool(sdscoordinator.value.school_id);
        console.log(school.value)
        await loadStudents(sdscoordinatorId);
    }
    loading.value = false;
});
</script>
  
<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
  