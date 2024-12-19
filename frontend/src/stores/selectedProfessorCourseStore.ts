import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as interfaces from "@/services/api/interfaces"

const baseURL = import.meta.env.VITE_API_URL;

export const useSelectedProfessorCourseStore = defineStore('selectedProfessorCourse', () => {
    const selectedCourse = ref<interfaces.Course>(); // holds the selectedCourse for professor, used for interactive navbar

    /**
     * Function To Get Value of Selected Course
     * @param course 
     */
    const setCourse = (course: interfaces.Course) => {
        selectedCourse.value = course;
    }

    /**
     * Function To Get Value of Selected Course
     */
    const getCourse = (): interfaces.Course => {
        return selectedCourse.value;
    }

    /**
     * Function To Get ID Value of Selected Course
     */
    const getCourseID = (): String => {
        return selectedCourse.value.id;
    }

    return {
        selectedCourse,
        setCourse,
        getCourse,
        getCourseID
    }
})