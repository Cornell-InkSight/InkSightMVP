
/**
 * Represents A User
 */
export interface User {
    user_ptr_id?: string;
    name: string;
    school_id: string,
    email?: string,
}

/**
 * Represents a student.
 */
export interface Student extends User {
    sds_coordinator_id: string,
    disability: string,
    year: string,
    accodomation_request: string,
}

/**
 * Represents an SDS Coordinator.
 */
export interface SDSCoordinator extends User {
    position?: string,
}

/**
 * Represents a professor.
 */
export interface Professor extends User {
    title?: string;
}

/**
 * Represents a TA
 */
export interface TA extends User {
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
    professors?: Professor[],
    cannotRequest?: string,
    term: string,
    course_uid: number,
    type: string,
    meeting_time: TimeRanges,
    campus: string,
    active?: boolean,
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
    notes: NotePacketEntry[],
    status: string,
    lectureData?: LectureSession,
}

export interface NotePacketEntry {
    id: string,
    type: string,
    value: string,
    url?: string,
}

/**
 * Represents a student notes packet
 */
export interface StudentNotePacket {
    id?: String,
    lecture_session_id: String,
    student_id: String,
    title: string,
    time: string,
    notes?: string,
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