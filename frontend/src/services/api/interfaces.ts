
/**
 * Represents a student.
 */
export interface Student {
    id?: string;
    name: string;
    sds_coordinator_id: string,
    school_id: string,
    disability: string
}

/**
 * Represents an SDS Coordinator.
 */
export interface SDSCoordinator {
    id?: string;
    name: string;
}

/**
 * Represents a professor.
 */
export interface Professor {
    id?: string;
    name: string;
    title: string;
}

/**
 * Represents a TA
 */
export interface TA {
    id?: string;
    name: string,
    professor_id: string,
}

/**
 * Represents a school.
 */
export interface School {
    id?: string;
    name: string;
}

/**
 * Represents a school.
 */
export interface ProfessorCourse {
    id?: string;
    professor_id: string;
    course_id: string;
}


/**
 * Represents a course.
 */
export interface Course {
    id?: string;
    name: string;
    sds_coordinator_id: string;
}

/**
 * Represents a new student-course
 */
export interface StudentCourse {
    id?: string,
    student_id: string,
    course_id: string
}
  
/**
 * Represents a course.
 */
export interface newCourse {
    id?: string;
    name: string;
    school_id: string,
    sds_coordinator_id: string;
}

/**
 * Represents a lecture session
 */
export interface LectureSession {
    id?: String,
    date: Date,
    course_id: Number,
    status: string
}

/**
 * Represents a notes packet
 */
export interface NotesPacket {
    id?: String,
    lecture_session_id: String,
    course_id: String,
    notes: string,
    status: string,
}

/**
 * Represents NoteTakingRequest
 */
export interface NoteTakingRequest {
    id?: string;
    request: string,
    student_course_id: string,
    sds_coordinator_id: string
}