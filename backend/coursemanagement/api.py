from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course, StudentCourse, ProfessorCourse
from .serializers import CourseSerializer, StudentCourseSerializer, ProfessorCourseSerializer
from usermanagement.models import Professor, Student, SDSCoordinator, TeacherAssistant
from usermanagement.serializers import StudentSerializer, ProfessorSerializer, SDSCoordinatorSerializer, TeacherAssistantSerializer
from django.shortcuts import render
from rest_framework import status

"""
GET (Course) Methods
Provides methods for retrieving information about courses, student-course relationships, and professor-course relationships.
Each function:
1. Queries the database using Django's ORM.
2. Serializes the data to native Python types (dictionaries) for conversion to JSON.
3. Returns the data as an HTTP response in JSON format.
4. Uses try-except blocks to handle cases where specific entries are not found.
"""

@api_view(["GET"])
def get_courses(request):
    """
    Retrieve all courses.
    Fetches all courses in the database and returns them as a JSON response.
    """
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_course(request, course_id):
    """
    Retrieve a specific course by ID.
    Args:
        course_id (int): The ID of the course to retrieve.
    Returns:
        JSON response containing course data if found; otherwise, a 404 error.
    """
    try:
        course = Course.objects.get(id=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Course does not exist in the database"}, status=404)

@api_view(["GET"])
def get_student_courses(request):
    """
    Retrieve all student-course relationships.
    Returns all records linking students to their courses.
    """
    student_courses = StudentCourse.objects.all()
    serializer = StudentCourseSerializer(student_courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_student_course(request, student_id, course_id):
    """
    Retrieve a specific student-course relationship by student and course ID.
    Args:
        student_id (int): The ID of the student.
        course_id (int): The ID of the course.
    """
    try:
        student_course = StudentCourse.objects.get(student_id=student_id, course_id=course_id)
        serializer = StudentCourseSerializer(student_course)
        return Response(serializer.data)
    except StudentCourse.DoesNotExist:
        return Response({"error": "Student-Course entry does not exist"}, status=404)

@api_view(["GET"])
def get_student_course_with_id(request, studentcourse_id):
    """
    Retrieve a specific student-course relationship by Student-Course ID.
    Args:
        studentcourse_id (int): The ID of the student-course.
    """
    try:
        student_course = StudentCourse.objects.get(id=studentcourse_id)
        serializer = StudentCourseSerializer(student_course)
        return Response(serializer.data)
    except StudentCourse.DoesNotExist:
        return Response({"error": "Student-Course entry does not exist"}, status=404)

@api_view(["GET"])
def get_professor_courses(request):
    """
    Retrieve all professor-course relationships.
    Returns all records linking professors to their courses.
    """
    professor_courses = ProfessorCourse.objects.all()
    serializer = ProfessorCourseSerializer(professor_courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_professor_course(request, professor_id, course_id):
    """
    Retrieve a specific professor-course relationship by professor and course ID.
    Args:
        professor_id (int): The ID of the professor.
        course_id (int): The ID of the course.
    """
    try:
        professor_course = ProfessorCourse.objects.get(professor_id=professor_id, course_id=course_id)
        serializer = ProfessorCourseSerializer(professor_course)
        return Response(serializer.data)
    except ProfessorCourse.DoesNotExist:
        return Response({"error": "Professor-Course entry does not exist"}, status=404)

@api_view(["GET"])
def get_all_courses_for_student(request, student_id):
    """
    Retrieve all courses associated with a specific student.
    Args:
        student_id (int): The ID of the student.
    Returns:
        JSON response containing courses associated with the student, or an error message.
    """
    student_courses = StudentCourse.objects.filter(student_id=student_id)
    course_ids = student_courses.values_list("course_id", flat=True).distinct()
    courses = Course.objects.filter(id__in=course_ids)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_courses_for_professor(request, professor_id):
    """
    Retrieve all courses associated with a specific student.
    Args:
        professor_id (int): The ID of the professor.
    Returns:
        JSON response containing courses associated with the student, or an error message.
    """
    professor_courses = ProfessorCourse.objects.filter(professor_id=professor_id)
    course_ids = professor_courses.values_list("course_id", flat=True).distinct()
    courses = Course.objects.filter(id__in=course_ids)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_professors_for_courses(request, course_id):
    """
    Retrieve all professors associated with a specific course.
    Args:
        course_id (int): The ID of the course.
    Returns:
        JSON response containing professors associated with the course, or an error message.
    """
    professor_courses = ProfessorCourse.objects.filter(course_id=course_id)
    professor_ids = professor_courses.values_list("professor_id", flat=True).distinct()
    professors = Professor.objects.filter(id__in=professor_ids)
    serializer = ProfessorSerializer(professors, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_courses_for_ta(request, ta_id):
    """
    Retrieve all courses associated with a specific ta.
    Args:
        ta_id (int): The ID of the ta.
    Returns:
        JSON response containing courses associated with the ta, or an error message.
    """
    ta = Professor.objects.get(id=ta_id)
    professor = Professor.objects.get(id=ta.professor_id)
    ta_courses = ProfessorCourse.objects.filter(professor_id=professor.id)
    course_ids = ta_courses.values_list("course_id", flat=True).distinct()
    courses = Course.objects.filter(id__in=course_ids)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_tas_for_courses(request, course_id):
    """
    Retrieve all professors associated with a specific course.
    Args:
        course_id (int): The ID of the course.
    Returns:
        JSON response containing tas associated with the course, or an error message.
    """
    professor_courses = ProfessorCourse.objects.filter(course_id=course_id)
    professor_ids = professor_courses.values_list("professor_id", flat=True).distinct()
    tas = TeacherAssistant.objects.filter(professor_id__in=professor_ids)
    serializer = TeacherAssistantSerializer(tas, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_students_for_professor(request, professor_id):
    """
    Retrieve all students enrolled in a professor's courses.
    Args:
        professor_id (int): The ID of the professor.
    Returns:
        JSON response containing a dictionary with course names as keys and lists of students as values.
    """
    professor_courses = ProfessorCourse.objects.filter(professor_id=professor_id)
    course_ids = professor_courses.values_list("course_id", flat=True).distinct()
    courses = Course.objects.filter(id__in=course_ids)

    course_students_dict = {}

    for course in courses:
        student_courses = StudentCourse.objects.filter(course_id = course.id)
        student_ids = student_courses.values_list("student_id", flat=True).distinct()
        students = Student.objects.filter(id__in = student_ids)

        serializer = StudentSerializer(students, many=True)
        course_students_dict[course.id] = serializer.data
    
    return Response(course_students_dict)

@api_view(["GET"])
def get_all_students_for_sds_coordinator(request, sds_coordinator_id):
    """
    Retrieve all students associated with courses overseen by an SDS coordinator.
    Args:
        sds_coordinator_id (int): The ID of the SDS coordinator.
    Returns:
        JSON response with student data or a 404 error if none found.
    """
    courses = Course.objects.filter(sds_coordinator_id=sds_coordinator_id)
    student_courses = StudentCourse.objects.filter(course_id__in=courses)
    student_ids = student_courses.values_list("student_id", flat=True).distinct()
    students = Student.objects.filter(id__in=student_ids)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_sds_coordinator_course(request, course_id):
    """
    Retrieve the respective SDS Coordinator associated with the courses overseen
    Args:
        course_id (int): the ID of the course
    Returns
        JSON response with the SDS coordinator data or 404 error if not found
    """
    course = Course.objects.get(id=course_id)
    sds_coordinator = SDSCoordinator.objects.get(id=course.sds_coordinator_id)
    serializer = SDSCoordinatorSerializer(sds_coordinator)
    return Response(serializer.data)

"""
POST (Course) Methods
Handles the creation of new entries in the database.
Each function:
1. Retrieves JSON data from the request.
2. Validates that all required fields are provided.
3. Creates the object, serializes it, and returns it in the response.
"""

@api_view(['POST'])
def add_course(request):
    """
    Add a new course to the database.
    Expected JSON fields: name, school_id, sds_coordinator_id.
    """
    course_data = request.data
    required_fields = ["name", "school_id", "sds_coordinator_id"]
    for field in required_fields:
        if field not in course_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
    course = Course.objects.create(
        name=course_data["name"],
        school_id=course_data["school_id"],
        sds_coordinator_id=course_data["sds_coordinator_id"]
    )
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=201)

@api_view(['POST'])
def add_student_course(request):
    """
    Add a new student-course entry to associate a student with a course.
    Expected JSON fields: name, student_id, course_id.
    """
    student_course_data = request.data
    required_fields = ["name", "student_id", "course_id"]
    for field in required_fields:
        if field not in student_course_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
    student_course = StudentCourse.objects.create(
        name=student_course_data["name"],
        student_id=student_course_data["student_id"],
        course_id=student_course_data["course_id"]
    )
    serializer = StudentCourseSerializer(student_course)
    return Response(serializer.data, status=201)

@api_view(['POST'])
def add_professor_course(request):
    """
    Add a new professor-course entry to associate a professor with a course.
    Expected JSON fields: name, professor_id, course_id.
    """
    professor_course_data = request.data
    required_fields = ["professor_id", "course_id"]
    for field in required_fields:
        if field not in professor_course_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
    professor_course = ProfessorCourse.objects.create(
        professor_id=professor_course_data["professor_id"],
        course_id=professor_course_data["course_id"]
    )
    serializer = ProfessorCourseSerializer(professor_course)
    return Response(serializer.data, status=201)

@api_view(['POST'])
def add_course_for_student(request, student_id):
    """
    Link an existing or new course to a specific student.
    Expected JSON fields: name, school_id, sds_coordinator_id.
    """
    course_data = request.data
    required_fields = ["name", "school_id", "sds_coordinator_id"]
    
    for field in required_fields:
        if field not in course_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)

    course = Course.objects.filter(
        name=course_data["name"],
        school_id=course_data["school_id"]
    ).first()

    if not course:
        course = Course.objects.create(
            name=course_data["name"],
            school_id=course_data["school_id"],
            sds_coordinator_id=course_data["sds_coordinator_id"]
        )

    if StudentCourse.objects.filter(student=student, course=course).exists():
        return Response({"error": "Student is already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

    student_course = StudentCourse.objects.create(student=student, course=course)

    return Response({
        "course": CourseSerializer(course).data,
        "student_course": StudentCourseSerializer(student_course).data
    }, status=status.HTTP_201_CREATED)
