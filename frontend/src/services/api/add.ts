import axios from "axios";
import authAxios from '@/services/api/setup';

import * as interfaces from './interfaces'
import { fetchSDSCoordinatorForCourses } from './fetch'

/**
 * Adds New Student Data Given Request
 * @param {Course} newCourse - The request data for the course.
 * @returns {Promise<void>} - A Promise that resolves to an object when the new course is added
 */

const baseURL = import.meta.env.VITE_API_URL;

export const addNewCourseForStudent = async (student_id: Number, newCourse: interfaces.newCourse) => {
    try {
        const response = await authAxios.post(`${baseURL}/coursemanagement/students/${student_id}/courses/add/`, newCourse);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add course", error);
        throw new Error("Failed to add course. Please check the provided data and try again.");
    }
}

/**
 * Adds a new lecture session by calling the API.
 * 
 * @param {interfaces.LectureSession} lectureSession - The details of the lecture session to add.
 * @returns {Promise<Object>} - A Promise that resolves to the response data when the lecture session is added.
 * @throws {Error} - Throws an error if the API request fails.
 */
export const addLectureSession = async (lectureSession: interfaces.LectureSession): Promise<Object> => {
    try {
        console.log("Sending lecture session data:", lectureSession);
        const response = await authAxios.post(`${baseURL}/lecturesessionsmanagement/lecture-sessions/add/`, lectureSession);
        return response.data;
    } 
    catch (error: any) {
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add course: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add course:", error.message);
            throw new Error("Failed to add course. Please check the provided data and try again.");
        }
    }
};


/**
 * Adds a Note-taking request by calling the API.
 * 
 * @param {string} student_id - The ID of the student making the note-taking request.
 * @param {string} course_id - The ID of the course for which the student is requesting note-taking.
 * @param {string} request - Details of the note-taking request.
 * @returns {Promise<Object>} - A Promise that resolves to the response data when the request is successfully created.
 * @throws {Error} - Throws an error if the API request fails.
 */
export const addNoteTakingRequest = async (student_id: string, course_id: string, request: string): Promise<Object> => {
    try {
        const { data: sdsCoordinator } = await fetchSDSCoordinatorForCourses(course_id);

        // Construct the note-taking request payload
        const note_taking_request = {
            request,
            student_id,
            course_id,
            sdscoordinator_id: sdsCoordinator ? sdsCoordinator.user_ptr_id : 1
        };
        console.log(note_taking_request)
        // Send the request to the server
        const response = await authAxios.post(`${baseURL}/notetakingrequestmanagement/notetaking-request/add/`, note_taking_request);
        
        return response.data;
    } catch (error: any) {
        // Enhanced error logging
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add note-taking request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add note-taking request:", error.message);
            throw new Error("Failed to add note-taking request. Please check the provided data and try again.");
    
        }
    }
};

/**
 * Approves note-taking request by calling API
 * @param notetakingrequest_id - the ID of the notetaking request to approve
 */
export const approveNoteTakingRequest = async (notetakingrequest_id: string) => {
    try {
        const response = await authAxios.put(`${baseURL}/notetakingrequestmanagement/notetaking-request/${notetakingrequest_id}/approve`)
        return response.data;
    } catch (error: any) {
        // Enhanced error logging
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add note-taking request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add note-taking request:", error.message);
            throw new Error("Failed to add note-taking request. Please check the provided data and try again.");
    
        }
    }
}

/**
 * Adds a new lecture session by calling API
 * @param lectureSession - the LectureSession Object to be inputted into database
 */
export const addNewLectureSession = async(lectureSession: interfaces.LectureSession) => {
    try {
        const response = await authAxios.post(`${baseURL}/lecturesessionsmanagement/lecture-sessions/add/`, lectureSession)
        return response.data;
    } catch (error: any) {
        // Enhanced error logging
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add status of lecture session request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add status of lecture session request:", error.message);
            throw new Error("Failed to add status of lecture session request. Please check the provided data and try again.");
    
        }
    }
}

/**
 * Set Status of lecture session by calling API
 * @param status - Status can be either "recording", "editing", "published"
 */
/**
 * Approves status of lecture session request by calling API
 * @param notetakingrequest_id - the ID of the notetaking request to approve
 */
export const updateStatusOfLecture = async (lecturesession_id: string, status: string) => {
    try {
        const response = await authAxios.put(`${baseURL}/lecturesessionsmanagement/lecture-sessions/${lecturesession_id}/update`, { "status": status })
        return response.data;
    } catch (error: any) {
        // Enhanced error logging
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add status of lecture session request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add status of lecture session request:", error.message);
            throw new Error("Failed to add status of lecture session request. Please check the provided data and try again.");
    
        }
    }
}
/**
 * Adds new note-taking packet by calling the API
 * @param {NotesPacket} notespacket - the notepacket to be added to the API
 */
export const addNewNotesPacket = async(notepacket: interfaces.NotesPacket) => {
    try {
        const response = await authAxios.post(`${baseURL}/notepacketsmanagement/notes-packets/add/`, notepacket)
        return response.data;
    } catch (error: any) {
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add status of lecture session request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add status of lecture session request:", error.message);
            throw new Error("Failed to add status of lecture session request. Please check the provided data and try again.");
    
        }
    }
}

/**
 * Set Status of note packet by calling API
 * @param status - Status can be either "recording", "editing", "published"
 */
/**
 * Approves status of note packet request by calling API
 * @param notetakingrequest_id - the ID of the notetaking request to approve
 */
export const updateStatusOfNotePacket = async (notepacket_id: string, status: string) => {
    try {
        const response = await authAxios.post(`${baseURL}/notepacketsmanagement/notes-packet/${notepacket_id}/update`, { "status": status })
        return response.data;
    } catch (error: any) {
        // Enhanced error logging
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add status of note packet request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add status of note packet request:", error.message);
            throw new Error("Failed to add status of note packet request. Please check the provided data and try again.");
    
        }
    }
}

/**
 * Update text of note packet by calling API
 * @param text - New text
 */
/**
 * Approves status of note packet request by calling API
 * @param notetakingrequest_id - the ID of the notetaking request to approve
 */
export const updateTextOfNotePacket = async (notepacket_id: string, text: string) => {
    try {
        const response = await authAxios.post(`${baseURL}/notepacketsmanagement/notes-packet/${notepacket_id}/edit`, { "text": text })
        return response.data;
    } catch (error: any) {
        // Enhanced error logging
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add text of note packet request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add text of note packet request:", error.message);
            throw new Error("Failed to add text of note packet request. Please check the provided data and try again.");
    
        }
    }
}

/**
 * Add New professor-course relation
 * @param 
 * @param notetakingrequest_id - the ID of the notetaking request to approve
 */
export const addNewProfessorCourse = async (data: interfaces.ProfessorCourse) => {
    try {
        const response = await authAxios.post(`${baseURL}/coursemanagement/professor-courses/add/`, data)
        return response.data;
    } catch (error: any) {
        // Enhanced error logging
        if (error.response) {
            console.error("Server responded with an error:", error.response.data);
            throw new Error(`Failed to add status of lecture session request: ${error.response.data.error || "Unknown server error"}`);
        } else {
            console.error("Failed to add status of lecture session request:", error.message);
            throw new Error("Failed to add status of lecture session request. Please check the provided data and try again.");
    
        }
    }
}

/**
 * Add New student 
 * @param 
 * @param newStudent - the data containing info of the new student
 */
export const addStudent = async (newStudent: interfaces.Student) => {
    try {
        const response = await authAxios.post(`${baseURL}/usermanagement/students/add`, newStudent);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add student", error);
        throw new Error("Failed to add student. Please check the provided data and try again.");
    }
}

/**
 * Add New professor 
 * @param 
 * @param newProfessor - the data containing info of the new Professor
 */
export const addProfessor = async (newProfessor: interfaces.Professor) => {
    try {
        const response = await authAxios.post(`${baseURL}/usermanagement/professors/add`, newProfessor);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add professor", error);
        throw new Error("Failed to add professor. Please check the provided data and try again.");
    }
}

/**
 * Add New sds coordinator 
 * @param newSDSCoordinator - the data containing info of the new SDSCoordinator
 */
export const addSDSCoordinator = async (newSDSCoordinator: interfaces.SDSCoordinator) => {
    try {
        const response = await authAxios.post(`${baseURL}/usermanagement/sdscoordinators/add`, newSDSCoordinator);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add SDS Coordinator", error);
        throw new Error("Failed to add SDS Coordinator. Please check the provided data and try again.");
    }
}

/**
 * Add New sds coordinator 
 * @param newTA - the data containing info of the new TA
 */
export const addTA = async (newTA: interfaces.TA) => {
    try {
        const response = await authAxios.post(`${baseURL}/usermanagement/tas/add`, newTA);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add TA", error);
        throw new Error("Failed to add TA. Please check the provided data and try again.");
    }
}

/**
 * Add New sds coordinator 
 * @param newCourse - the data containing info of the new Course
 */
export const addCourse = async (newCourse: interfaces.Course) => {
    console.log(newCourse)
    try {
        const response = await authAxios.post(`${baseURL}/coursemanagement/courses/add/`, newCourse);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add course", error);
        throw new Error("Failed to add course. Please check the provided data and try again.");
    }
}

/**
 * Add New sds coordinator 
 * @param newCourse - the data containing info of the new Course
 */
export const addStudentToCourse = async (studentId: Number, courseId: Number) => {
    try {
        const response = await authAxios.post(`${baseURL}/coursemanagement/students/${studentId}/${courseId}/add/`);
        return response.data;
    } 
    catch(error) {
        console.error("Failed to add course", error);
        throw new Error("Failed to add course. Please check the provided data and try again.");
    }
}

