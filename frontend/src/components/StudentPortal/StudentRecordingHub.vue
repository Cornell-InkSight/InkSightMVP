<template>
<!-- Popup Container -->
<div class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
    <!-- Conditional Popup Content -->
    <div v-if="ongoingLecture">
        <!-- Ongoing Lecture Details -->
        <h2 class="text-xl font-bold mb-4 text-gray-900">Ongoing Lecture</h2>
        <p class="text-sm text-gray-600 mb-2">
        <strong>Lecture Title:</strong> {{ ongoingLecture.title }}
        </p>
        <p class="text-sm text-gray-600 mb-4">
        <strong>Course:</strong> {{ course.name }}
        </p>
        <!-- Buttons -->
        <div class="flex justify-end space-x-4">
        <button
            @click="goBack"
            class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
        >
            Cancel
        </button>
        <button
            @click="joinLecture"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
            Join
        </button>
        </div>
    </div>

    <div v-else>
        <!-- No Ongoing Lecture -->
        <h2 class="text-xl font-bold mb-4 text-gray-900">No Ongoing Lecture Session</h2>
        <p class="text-sm text-gray-600 mb-4">
        There is currently no ongoing lecture session.
        </p>
        <!-- Back Button -->
        <div class="flex justify-end">
        <button
            @click="goBack"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
            Back
        </button>
        </div>
    </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { fetchCurrentOngoingLectureSession, fetchCourse, fetchCourses } from "@/services/api/fetch";
import * as interfaces from "@/services/api/interfaces"

const router = useRouter();
const route = useRoute();
const ongoingLecture = ref(null); // Holds the ongoing lecture session data (if any)
const course = ref<interfaces.Course>(); // Holds the course data

/**
 * Navigates back to the previous page.
 */
const goBack = () => {
    router.back();
};

/**
 * Redirects to the lecture session view.
 */
const joinLecture = () => {
    if (ongoingLecture.value) {
        router.push(`/students/${route.params.studentId}/${course.value.id}/lecture`);
    }
};

/**
 * Loads course names for each course ID in `studentscourses`.
 */
const loadCourse = async (courseId: string): Promise<void> => {
    const { data, error: fetchError } = await fetchCourse(courseId);
    if (!fetchError && data) {
        course.value = data;
    } else {
        console.error(`Failed to fetch course name for course ID ${courseId}:`, fetchError);
    }
};


/**
 * Fetches and sets ongoing lecture session data (if any).
 */
 const checkOngoingLecture = async (courseId: string) => {
  try {
    const { data, error } = await fetchCurrentOngoingLectureSession(courseId);
    if (data) {
      ongoingLecture.value = data;
      return true; // Return true if an ongoing lecture is found
    } else if (error) {
      console.error(`No ongoing lecture session for course ID ${courseId}:`, error);
      return false; // Return false if no ongoing lecture is found
    }
  } catch (err) {
    console.error(`Error checking ongoing lecture for course ID ${courseId}:`, err);
    return false;
  }
};

/**
 * Lifecycle hook to fetch required data.
 * Fetches student courses, then iterates and checks if any course has ongoing lecture
 */
onMounted(async () => {
  const studentId = route.params.studentId as string;

  const { data: courses, error: coursesError } = await fetchCourses(studentId);

  if (coursesError) {
    console.error("Error fetching courses for the student:", coursesError);
    return;
  }

  if (courses && courses.length > 0) {
    for (const course of courses) {
      await loadCourse(course.id);

      const hasOngoingLecture = await checkOngoingLecture(course.id);
      console.log(hasOngoingLecture)
      if (hasOngoingLecture) {
        break;
      }
    }
  } else {
    console.error("No courses found for the student.");
  }
});
</script>

<style scoped>
    /* Fade Transition Styles */
    .fade-enter-active,
    .fade-leave-active {
    transition: opacity 0.3s ease;
    }
    .fade-enter-from,
    .fade-leave-to {
    opacity: 0;
}
</style>
  