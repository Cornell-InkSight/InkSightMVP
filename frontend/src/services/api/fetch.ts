import axios from 'axios';

/**
 * Represents a student.
 */
interface Student {
  id: string;
  name: string;
}

/**
 * Represents an SDS Coordinator.
 */
interface SDSCoordinator {
  id: string;
  name: string;
}

/**
 * Represents a professor.
 */
interface Professor {
  id: string;
  name: string;
  title: string;
}

/**
 * Represents a school.
 */
interface School {
  id: string;
  name: string;
}

/**
 * Represents a course.
 */
interface Course {
  id: string;
  name: string;
  sdscoordinator: string;
}

/**
 * Fetches students associated with a specific SDS coordinator.
 * @param {string} sdscoordinatorId - The ID of the SDS coordinator.
 * @returns {Promise<{ data: Student[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchStudentsForSDSCoordinators = async (sdscoordinatorId: string): Promise<{ data: Student[] | null, error: string | null }> => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/coursemanagement/sdscoordinators/${sdscoordinatorId}/students`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load students" };
  }
};

/**
 * Fetches students associated with a specific professor.
 * @param {string} professorId - The ID of the professor.
 * @returns {Promise<{ data: Student[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of students or an error message.
 */
export const fetchStudentsForProfessors = async (professorId: string): Promise<{ data: Student[] | null, error: string | null }> => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/coursemanagement/professors/${professorId}/students`);
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
export const fetchProfessor = async (professorId: string): Promise<{ data: Professor | null, error: string | null }> => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/usermanagement/professors/${professorId}`);
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
export const fetchSDSCoordinator = async (sdscoordinatorId: string): Promise<{ data: SDSCoordinator | null, error: string | null }> => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/usermanagement/sdscoordinators/${sdscoordinatorId}`);
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
export const fetchSchool = async (schoolId: string): Promise<{ data: School | null, error: string | null }> => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/schoolmanagement/schools/${schoolId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load school" };
  }
};

/**
 * Fetches details for a specific student.
 * @param {string} studentId - The ID of the student.
 * @returns {Promise<{ data: Student | null; error: string | null }>} - A Promise that resolves to an object containing either a student or an error message.
 */
export const fetchStudent = async (studentId: string): Promise<{ data: Student | null; error: string | null }> => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/usermanagement/students/${studentId}`);
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load student" };
  }
};

/**
 * Fetches courses for a specific student.
 * @param {string} studentId - The ID of the student.
 * @returns {Promise<{ data: Course[] | null; error: string | null }>} - A Promise that resolves to an object containing either an array of courses or an error message.
 */
export const fetchCourses = async (studentId: string): Promise<{ data: Course[] | null; error: string | null }> => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/coursemanagement/students/${studentId}/courses/`);
    console.log("Courses data:", JSON.stringify(response.data, null, 2));
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: "Failed to load courses" };
  }
};
