import axios from "axios";
import * as interfaces from './interfaces'
import { fetchSDSCoordinatorForCourses } from './fetch'

/**
 * Adds New Student Data Given Request
 * @param {Course} newCourse - The request data for the course.
 * @returns {Promise<void>} - A Promise that resolves to an object when the new course is added
 */

export const addCourseForStudent = async (student_id: Number, newCourse: interfaces.newCourse) => {
    try {
        const response = await axios.post(`http://127.0.0.1:8000/coursemanagement/students/${student_id}/courses/add/`, newCourse);
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
        const response = await axios.post(`http://127.0.0.1:8000/lecturesessionsmanagement/lecture-sessions/add/`, lectureSession);
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

import axios from 'axios';

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
            sdscoordinator_id: sdsCoordinator.id
        };

        // Send the request to the server
        const response = await axios.post("http://127.0.0.1:8000/notetakingrequestmanagement/notes-packets/add/", note_taking_request);
        
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

