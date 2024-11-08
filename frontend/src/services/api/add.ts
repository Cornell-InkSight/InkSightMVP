import axios
 from "axios";
/**
 * Represents a course.
 */
interface newCourse {
    name: string;
    school_id: string,
    sdscoordinator_id: string;
}
  

  /**
 * Adds New Student Data Given Request
 * @param {Course} newCourse - The request data for the course.
 * @returns {Promise<void>} - A Promise that resolves to an object when the new course is added
 */

export const addCourseForStudent = async (student_id: Number, newCourse: newCourse) => {
    try {
        const response = await axios.post(`http://127.0.0.1:8000/coursemanagement/students/${student_id}/courses/add/`, newCourse);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add course", error);
        throw new Error("Failed to add course. Please check the provided data and try again.");
    }
}
