
/**
 * Represents a student.
 */
export interface Student {
    id: string;
    name: string;
}

/**
 * Represents an SDS Coordinator.
 */
export interface SDSCoordinator {
    id: string;
    name: string;
}

/**
 * Represents a professor.
 */
export interface Professor {
    id: string;
    name: string;
    title: string;
}

/**
 * Represents a school.
 */
export interface School {
    id: string;
    name: string;
}

/**
 * Represents a course.
 */
export interface Course {
    id: string;
    name: string;
    sdscoordinator: string;
}
  
/**
 * Represents a course.
 */
export interface newCourse {
    name: string;
    school_id: string,
    sdscoordinator_id: string;
}

/**
 * Represents a lecture session
 */
export interface LectureSession {
    date: string,
    course_id: Number,
    notespacket: URL,
    status: string
}

/**
 * Represents a notes packet
 */
export interface NotesPacket {
    lecture_session_id: Number,
    
}

/**
 * Represents NoteTakingRequest
 */
export interface NoteTakingRequest {
    request: string,
    student_course_id: string,
    sdscoordinator_id: string
}