from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course, StudentCourse
from .serializers import CourseSerializer, StudentCourseSerializer
from usermanagement.models import Professor, Student
from usermanagement.serializers import StudentSerializer
from django.shortcuts import render

"""
GET (Course) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""
@api_view(["GET"])
def get_courses(request):
    """Method to Fetch Courses"""
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_course(request, course_id):
    """Method to Fetch Course"""
    try:
        course = Course.objects.get(course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Course Does Not Exist in Database"}, 404)
    
@api_view(["GET"])
def get_student_courses(request):
    """Method to Fetch Student-Courses Intermediates"""
    student_courses = StudentCourse.objects.all()
    serializer = StudentCourseSerializer(student_courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_student_course(request, student_id, course_id):
    """Method to Fetch Student-Courses Intermediate"""
    try:
        student_course = StudentCourse.objects.get(student_id=student_id, course_id=course_id)
        serializer = StudentCourseSerializer(student_course)
        return Response(serializer.data)
    except StudentCourse.DoesNotExist:
        return Response({"error": "Course Doex Not Exist in Database"}, 404)

"""
GET (Course-User) Methods
1. Uses ORMs to query database, translating SQL to Python
2. find the specific courses that each student has, or professor/SDS Coordinator
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""
@api_view(["GET"])
def get_all_courses_for_student(request, student_id):
    """Method to Fetch All Courses For Specific Student"""
    try:
        student_courses = StudentCourse.objects.filter(student_id=student_id)
        course_ids = student_courses.values_list("course_id", flat=True).distinct()
        courses = Course.objects.filter(id__in=course_ids)
        serializer = StudentCourseSerializer(courses, many=True)
        return Response(serializer.data)
    except StudentCourse.DoesNotExist:
        return Response({"error": "Course Doex Not Exist in Database"}, 404)

@api_view(["GET"])
def get_all_students_for_professor(request, professor_id):
    """Method to Fetch Students for a Specific Professor's Courses"""
    try:
        courses = Course.objects.filter(professor_id=professor_id)
        student_courses = StudentCourse.objects.filter(course_id__in=courses)

        student_ids = student_courses.values_list("student_id", flat=True).distinct()
        students = Student.objects.filter(id__in=student_ids)
        
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=200)

    except Course.DoesNotExist:
        return Response({"error": "Professor does not exist or has no courses"}, status=404)

@api_view(["GET"])
def get_all_students_for_sds_coordinator(request, sds_coordinator_id):
    """Method To Fetch All Students for SDS Coordinator"""
    try:
        courses = Course.objects.filter(sds_coordinator_id=sds_coordinator_id)
        student_courses = StudentCourse.objects.filter(course_id__in=courses)

        student_ids = student_courses.values_list("student_id", flat=True).distinct()
        students = Student.objects.filter(id__in = student_ids)

        serializer = StudentSerializer(students)
        return Response(serializer.data, status=200)
    except Course.DoesNotExist:
        return Response({"error": "SDS Coordinator does not exist or has no courses"}, status=404)
    
"""
POST (Course) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_course(request):
    """Method to Add New course"""
    course_data = request.data

    required_fields = ["name", "school_id", "professor_id", "sds_coordinator_id"]
    for field in required_fields:
        if field not in course_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    course = course.objects.create(
        name=course_data["name"], 
        school_id=course_data["school_id"], 
        professor_id = course_data["professor_id"],
        sds_coordinator_id = course_data["sds_coordinator_id"]
    )

    serializer = CourseSerializer(course)
    return Response(serializer.data, status=201)    

@api_view(['POST'])
def add_student_course(request):
    """Method to Add New student_course"""
    student_course_data = request.data

    required_fields = ["name", "student_id", "course_id"]
    for field in required_fields:
        if field not in student_course_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    student_course = student_course.objects.create(
        name=student_course_data["name"], 
        student_id=student_course_data["student_id"],
        course_id =student_course_data["course_id"] 
    )

    serializer = StudentCourseSerializer(student_course)
    return Response(serializer.data, status=201)    

@api_view(['POST'])
def add_course_for_student(request, student_id):
    """
    Method to Add Existing or New Course for a Specific Student.
    If the course already exists, it only links the course with the student in StudentCourse.
    """
    course_data = request.data

    required_fields = ["name", "school_id", "professor_id", "sds_coordinator_id"]
    for field in required_fields:
        if field not in course_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)

    course, created_course = Course.objects.get_or_create(
        name=course_data["name"],
        school_id=course_data["school_id"],
        professor_id=course_data["professor_id"],
        sds_coordinator_id=course_data["sds_coordinator_id"]
    )

    if StudentCourse.objects.filter(student=student, course=course).exists():
        return Response({"error": "Student is already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

    # Link the course with the student in StudentCourse
    student_course = StudentCourse.objects.create(student=student, course=course)

    course_serializer = CourseSerializer(course)
    student_course_serializer = StudentCourseSerializer(student_course)

    return Response({
        "course": course_serializer.data,
        "student_course": student_course_serializer.data
    }, status=status.HTTP_201_CREATED)
