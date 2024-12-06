<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100">
    <!-- Error Message Box -->
   <div v-if="errorMessage" class="w-full max-w-md mb-4">
      <div class="bg-red-500 text-white text-sm font-bold p-3 rounded-md shadow-md">
        {{ errorMessage }}
      </div>
    </div>

  <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-3xl font-bold text-gray-900 text-center">Welcome to InkSight</h2>

    <!-- Tabs for Login and Sign Up -->
    <div class="flex space-x-4 border-b pb-2">
      <button
        class="flex-1 text-center font-semibold"
        :class="activeTab === 'login' ? 'border-blue-500 text-blue-500' : 'text-gray-700 hover:text-gray-900'"
        @click="setActiveTab('login')"
      >
        Login
      </button>
      <button
        class="flex-1 text-center font-semibold"
        :class="activeTab === 'signup' ? 'border-blue-500 text-blue-500' : 'text-gray-700 hover:text-gray-900'"
        @click="setActiveTab('signup')"
      >
        Sign Up
      </button>
    </div>

    

    <!-- Login Tab -->
    <div v-if="activeTab === 'login'">
      <div class="flex space-x-4 mb-4">
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'student' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('student')"
        >
          Student
        </button>
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'professor' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('professor')"
        >
          Professor
        </button>
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'teacher_assistant' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('teacher_assistant')"
        >
          TA
        </button>
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'sds_coordinator' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('sds_coordinator')"
        >
          SDS Coordinator
        </button>
      </div>
      <button
        class="w-full py-2 bg-black text-white font-semibold rounded-md hover:bg-gray-800"
        @click="redirectToGoogleLogin"
      >
        Login with Google
      </button>
    </div>

    <!-- Sign Up Tab -->
    <form v-if="activeTab === 'signup'" class="space-y-4" @submit.prevent="redirectToGoogle">
      <!-- Role Selection -->
      <div class="flex space-x-4">
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'student' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('student')"
        >
          Student
        </button>
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'professor' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('professor')"
        >
          Professor
        </button>
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'teacher_assistant' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('teacher_assistant')"
        >
          TA
        </button>
        <button 
          class="flex-1 py-2 border rounded-md font-semibold"
          :class="role === 'sds_coordinator' ? 'bg-blue-500 text-white border-blue-500' : 'text-gray-700 border-gray-300 hover:bg-gray-100'"
          @click="setRole('sds_coordinator')"
        >
          SDS Coordinator
        </button>
      </div>

      <!-- Role-Specific Fields -->
      <div>
        <label for="school" class="block text-sm font-medium text-gray-700">Select School</label>
        <select
          id="school"
          v-model="schoolId"
          required
          @change="role === 'teacher_assistant' ? loadSchoolProfessors(schoolId) : null"
          class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300"
        >
          <option value="" disabled>Select your school</option>
          <option v-for="school in schools" :key="school.id" :value="school.id">{{ school.name }}</option>
        </select>
      </div>
      <div v-if="role === 'student'">
        <label for="year" class="block text-sm font-medium text-gray-700">Year</label>
        <input type="number" id="year" v-model="year" required min="2024" max="2028" placeholder="Enter your year" class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300 mb-2" />
        <label for="disability" class="block text-sm font-medium text-gray-700">Disability</label>
        <input type="text" id="disability" v-model="disability" required placeholder="Enter your disability" class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300 mb-2" />
        <label for="sds_coordinator_access_code" class="block text-sm font-medium text-gray-700">Access Code</label>
        <input type="text" id="sds_coordinator_access_code" v-model="sds_coordinator_access_code" required placeholder="Enter the access code provided by your disability coordinator" class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300" />
      </div>
      <div v-if="role === 'professor'">
        <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
        <input type="text" id="title" v-model="title" required placeholder="Enter your title" class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300" />
      </div>
      <div v-if="role === 'teacher_assistant'">
        <label for="professor" class="block text-sm font-medium text-gray-700">Assign Professor</label>
        <select id="professor" v-model="professorId" required class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300">
          <option value="" disabled>Select your professor</option>
          <option v-for="professor in professors" :key="professor.user_ptr_id" :value="professor.user_ptr_id">{{ professor.name }}</option>
        </select>
      </div>
      <div v-if="role === 'sds_coordinator'">
        <label for="position" class="block text-sm font-medium text-gray-700">Position</label>
        <input type="text" id="position" v-model="position" required placeholder="Enter your position" class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300" />
      </div>

      <button type="submit" class="w-full py-2 bg-black text-white font-semibold rounded-md hover:bg-gray-800">
        Sign Up
      </button>
    </form>
  </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchProfessorsForSchools, fetchSchools } from "@/services/api/fetch"
import { useRoute } from "vue-router";
const errorMessage = ref<string | null>(null); 

const schoolName = ref("");
const year = ref("2024");
const disability = ref("");
const sds_coordinator_access_code = ref("");
const title = ref("");
const schoolId = ref("");
const position = ref("");
const professorId = ref("");
const role = ref("student");
const schools = ref([]);
const professors = ref([]);

const route = useRoute()

const setRole = (selectedRole: string) => {
  role.value = selectedRole;
};
const activeTab = ref("login");
const setActiveTab = (tab: string) => (activeTab.value = tab);

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
        return
    }
    professors.value = data
    console.log(professors)
}
const redirectToGoogle = () => {
  if (!role.value) {
    alert("Please select a role before proceeding.");
    return;
  }

  const queryParams = new URLSearchParams({
    role: role.value,
    year: role.value === "student" ? year.value : undefined,
    disability: role.value === "student" ? disability.value : undefined,
    sds_coordinator_access_code: role.value === "student" ? sds_coordinator_access_code.value : undefined,
    title: role.value === "professor" ? title.value : undefined,
    school_id: schoolId.value,
    professor_id: role.value === "teacher_assistant" ? professorId.value : undefined,
    position: role.value === "sds_coordinator" ? position.value : undefined,
  }).toString();

  window.location.href = `http://127.0.0.1:8000/usermanagement/google-signup/redirect/?${queryParams}`;
};

const redirectToGoogleLogin = () => {
  const queryParams = new URLSearchParams({
    role: role.value,
  }).toString();
  window.location.href = `http://127.0.0.1:8000/usermanagement/google-login/redirect/?${queryParams}`;
};

/**
 * Loads all schools for dropdown
 */
const loadSchool = async () => {
  const { data, error: fetchError } = await fetchSchools();
  if(fetchError) {
      console.error(fetchError)
      return
  }
  schools.value = data;
};

/**
 * Fetches the error from the URL if there is one
 */
const getErrorFromUrl = () => {
  const params = new URLSearchParams(window.location.search);
  const error = params.get("error");
  if (error) {
    errorMessage.value = decodeURIComponent(error);
  }
};

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for both the professor and their SDS coordinaotrs.
 */
 onMounted(async () => {
  await loadSchool();
  getErrorFromUrl();

})
</script>
