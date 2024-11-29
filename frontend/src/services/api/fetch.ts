import * as interfaces from '@/services/api/interfaces' 
import authAxios from '@/services/api/setup';
import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL;
/**
 * Fetches students associated with a specific SDS coordinator.
 * @param {string} sdscoordinatorId - The ID of the SDS coordinator.
 * @returns {Promise<{ data: Student[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchStudentsForSDSCoordinators = async (sdscoordinatorId: string): Promise<{ data: interfaces.Student[] | null, error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/sdscoordinators/${sdscoordinatorId}/students`);
    return { data: response.data, error: null }; 
  } catch (err) {
    return { data: null, error: "Failed to load students" };
  }
};

/**
 * Fetches students associated with a specific professor.
 * @param {string} professorId - The ID of the professor.
 * @returns {Promise<{ data: interfaces.Student[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchStudentsForProfessors = async (professorId: string): Promise<{ data: interfaces.Student[] | null, error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/professors/${professorId}/students`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load students" };
  }
};

/**
 * Fetches details for a specific professor.
 * @param {string} professorId - The ID of the professor.
 * @returns {Promise<{ data: Professor | null; error: string | null }>} - A Promise that resolves to an object containing either a professor or an error message.
 */
export const fetchProfessor = async (professorId: string): Promise<{ data: interfaces.Professor | null, error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/usermanagement/professors/${professorId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load Professor" };
  }
};

/**
 * Fetches details for a specific SDS coordinator.
 * @param {string} sdscoordinatorId - The ID of the SDS coordinator.
 * @returns {Promise<{ data: SDSCoordinator | null; error: string | null }>} - A Promise that resolves to an object containing either an SDS coordinator or an error message.
 */
export const fetchSDSCoordinator = async (sdscoordinatorId: string): Promise<{ data: interfaces.SDSCoordinator | null, error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/usermanagement/sdscoordinators/${sdscoordinatorId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load SDS Coordinator" };
  }
};

/**
 * Fetches details for a specific school.
 * @param {string} schoolId - The ID of the school.
 * @returns {Promise<{ data: School | null; error: string | null }>} - A Promise that resolves to an object containing either a school or an error message.
 */
export const fetchSchool = async (schoolId: string): Promise<{ data: interfaces.School | null, error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/schoolmanagement/schools/${schoolId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load school" };
  }
};

/**
 * Fetches details for a specific school.
 * @param {string} schoolId - The ID of the school.
 * @returns {Promise<{ data: School | null; error: string | null }>} - A Promise that resolves to an object containing either a school or an error message.
 */
export const fetchSchools = async (): Promise<{ data: interfaces.School[] | null, error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/schoolmanagement/schools/`);
    console.log(response.data)
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load schools" };
  }
};

/**
 * Fetches details for a specific student.
 * @param {string} studentId - The ID of the student.
 * @returns {Promise<{ data: Student | null; error: string | null }>} - A Promise that resolves to an object containing either a student or an error message.
 */
export const fetchStudent = async (studentId: string): Promise<{ data: interfaces.Student | null; error: string | null }> => {
  console.log(baseURL)
  try {
    const response = await authAxios.get(`${baseURL}/usermanagement/students/${studentId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load student" };
  }
};

/**
 * Fetches details for a specific student.
 * @param {string} taId - The ID of the TA.
 * @returns {Promise<{ data: Student | null; error: string | null }>} - A Promise that resolves to an object containing either a TA or an error message.
 */
export const fetchTA = async (taId: string): Promise<{ data: interfaces.TA | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/usermanagement/tas/${taId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load TA" };
  }
};

/**
 * Fetches courses for a specific student.
 * @param {string} studentId - The ID of the student.
 * @returns {Promise<{ data: Course[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchCourses = async (studentId: string): Promise<{ data: interfaces.Course[] | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/students/${studentId}/courses/`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load courses" };
  }
};

/**
 * Fetches course for a specific id.
 * @param {string} courseId - The ID of the course.
 * @returns {Promise<{ data: Course[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchCourse = async (courseId: string): Promise<{ data: interfaces.Course | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/courses/${courseId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load courses" };
  }
};

/**
 * Fetches details for a specific student.
 * @param {string} studentId - The ID of the student.
 * @returns {Promise<{ data: Student | null; error: string | null }>} - A Promise that resolves to an object containing either a student or an error message.
 */
export const fetchStudentCourses = async (studentcoursesid: string): Promise<{ data: interfaces.StudentCourse | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/student-courses/${studentcoursesid}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load student" };
  }
};

/**
 * Fetches courses for a specific school.
 * @param {string} schoolid - The ID of the school.
 * @returns {Promise<{ data: Course[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchCoursesForSchools = async (schoolid: string): Promise<{ data: interfaces.Course[] | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/schoolmanagement/schools/${schoolid}/courses`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load courses" };
  }
};


/**
 * Fetches courses for a specific school.
 * @param {string} schoolid - The ID of the school.
 * @returns {Promise<{ data: Course[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchProfessorsForSchools = async (schoolid: string): Promise<{ data: interfaces.Professor[] | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/schoolmanagement/schools/${schoolid}/professors`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load professors" };
  }
};


/**
 * Fetches courses for a specific professor.
 * @param {string} professorid - The ID of the professor.
 * @returns {Promise<{ data: Course[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchCoursesForProfessors = async (professorid: string): Promise<{ data: interfaces.Course[] | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/professors/${professorid}/courses`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load courses" };
  }
};



/**
 * Fetches professors for a specific course.
 * @param {string} courseid - The ID of the course.
 * @returns {Promise<{ data: Course[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchProfessorsForCourses = async (courseid: string): Promise<{ data: interfaces.Course[] | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/courses/${courseid}/professors`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load courses" };
  }
};

/**
 * Fetches SDS coordinator for a specific course.
 * @param {string} courseid - The ID of the course.
 * @returns {Promise<{ data: interfaces.SDSCoordinator | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchSDSCoordinatorForCourses = async (courseid: string): Promise<{ data: interfaces.SDSCoordinator | null; error: string | null }> => {
  try {
    const response = await authAxios.get(`${baseURL}/coursemanagement/courses/${courseid}/sdscoordinator`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load SDS Coordinator" };
  }
};


/**
 * Fetches Notes Packets for Respective Courses
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.NoteTakingRequest[] | null; error: string | null> } - A Promise that resolves to an object containing either an array of notes packets or an error message.
 */
export const fetchNotetakingRequestsForCourses = async (courseId: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notetakingrequestmanagement/courses/${courseId}/note-packets`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Taking Courses" }
  }
}


/**
 * Fetches All NOte Packets for Respective Course
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.NotesPacket[] | null; error: string | null> } - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchdNotePacketsForCourse = async (courseId: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notepacketsmanagement/courses/${courseId}/notes-packets`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Packets" }
  }
}

/**
 * Fetches All NOte Packets for Respective Course
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.NotesPacket[] | null; error: string | null> } - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchStudentNotePacketsForCourse = async (studentId: string, courseId: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notepacketsmanagement/students/${studentId}/${courseId}/student-note-packets`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Packets" }
  }
}


/**
 * Fetches Approved Students for Respective Course
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.Student[] | null; error: string | null> } - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchApprovedStudentsForCourse = async (courseId: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notetakingrequestmanagement/courses/${courseId}/approved-students`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Taking Courses" }
  }
}

/**
 * Fetches Unpublished NOte Packets for Respective Course
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.NotesPacket[] | null; error: string | null> } - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchUnpublishedNotePacketsForCourse = async (courseId: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notepacketsmanagement/courses/${courseId}/notes-packets-unpublished`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Packets" }
  }
}


/**
 * Fetches Published NOte Packets for Respective Course
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.NotesPacket[] | null; error: string | null> } - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchPublishedNotePacketsForCourse = async (courseId: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notepacketsmanagement/courses/${courseId}/notes-packets-published`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Packets" }
  }
}

/**
 * Fetches Published NOte Packets for Respective Course
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.NotesPacket | null; error: string | null> } - A Promise that resolves to an object containing either an array of note-packets or an error message.
 */
export const fetchNotePacket = async (note_packet_id: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notepacketsmanagement/notes-packets/${note_packet_id}/`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Packets" }
  }
}

/**
 * Fetches Published NOte Packets for Respective Course
 * @param {string} courseid - The id of the course
 * @returns {Promise <data: interfaces.NotesPacket | null; error: string | null> } - A Promise that resolves to an object containing either an array of note-packets or an error message.
 */
export const fetchStudentNotePacket = async (note_packet_id: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notepacketsmanagement/student-notes-packets/${note_packet_id}/`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Note Packets" }
  }
}



/**
 * Fetches If Student Has Approval for Note Packets for Course
 * @param {string} courseId - the id of the course
 * @param {string} studentId - the id of the student
 *  * @returns {Promise <data: interfaces.NotesPacket | null; error: string | null> } - A Promise that resolves to an object containing either a boolean or an error message.
 */
export const fetchIsApprovedStudentForCourse = async(student_id: string, course_id: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notetakingrequestmanagement/notetaking-request/${student_id}/${course_id}/approved`)
    return { data: response.data.approved, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Approval" }
  }
}

/**
 * Fetches If Student Has Pending for Note Packets for Course
 * @param {string} courseId - the id of the course
 * @param {string} studentId - the id of the student
 *  * @returns {Promise <data: interfaces.NotesPacket | null; error: string | null> } - A Promise that resolves to an object containing either a boolean or an error message.
 */
export const fetchIsPendingStudentForCourse = async(student_id: string, course_id: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notetakingrequestmanagement/notetaking-request/${student_id}/${course_id}/pending`)
    return { data: response.data.pending, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Approval" }
  }
}

/**
 * Fetches If Student Has Approval for Note Packets for Course
 * @param {string} courseId - the id of the course
 * @param {string} studentId - the id of the student
 *  * @returns {Promise <data: interfaces.NotesPacket | null; error: string | null> } - A Promise that resolves to an object containing either a boolean or an error message.
 */
export const fetchNoteTakingRequestStudentForCourse = async(student_id: string, course_id: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/notetakingrequestmanagement/notetaking-request/${student_id}/${course_id}/`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Approval" }
  }
}

/**
 * Fetches If Current Lectyre Ongoing for Course
 * @param {string} courseId - the id of the course
 *  * @returns {Promise <data: interfaces.LectureSession | null; error: string | null> } - A Promise that resolves to an object containing either a boolean or an error message.
 */
export const fetchCurrentOngoingLectureSession = async(course_id: string) => {
  try {
    const response = await authAxios.get(`${baseURL}/lecturesessionsmanagement/${course_id}/current-lecture-session`)
    return { data: response.data, error: null }
  } catch(err) {
    return { data: null, error: "Failed to load Approval" }
  }
}
