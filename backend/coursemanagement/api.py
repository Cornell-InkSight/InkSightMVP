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
def get_courses():
    """Method to Fetch Courses"""
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_course(course_id):
    """Method to Fetch Course"""
    try:
        course = Course.objects.get(course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Course Does Not Exist in Database"}, 404)
    
@api_view(["GET"])
def get_student_courses():
    """Method to Fetch Student-Courses Intermediates"""
    student_courses = StudentCourse.objects.all()
    serializer = StudentCourseSerializer(student_courses, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_student_course(student_id, course_id):
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
def get_all_courses_for_student(student_id):
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
def get_all_students_for_professor(professor_id):
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
def get_all_students_for_sds_coordinator(sds_coordinator_id):
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