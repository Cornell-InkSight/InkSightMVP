from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course, StudentCourse
from .serializers import CourseSerializer, StudentCourseSerializer
from django.shortcuts import render

"""
GET (Course) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""
def get_courses():
    """Method to Fetch Courses"""
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

def get_course(course_id):
    """Method to Fetch Course"""
    try:
        course = Course.objects.prefetch_related(course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Course Does Not Exist in Database"}, 404)
    

def get_student_courses():
    """Method to Fetch Student-Courses Intermediates"""
    student_courses = StudentCourse.objects.all()
    serializer = StudentCourseSerializer(student_courses, many=True)
    return Response(serializer.data)

def get_student_course(student_id, course_id):
    """Method to Fetch Student-Courses Intermediate"""
    try:
        student_course = StudentCourse.objects.prefetch_related(student_id=student_id, course_id=course_id)
        serializer = StudentCourseSerializer(student_course)
        return Response(serializer.data)
    except StudentCourse.DoesNotExist:
        return Response({"error": "Course Doex Not Exist in Database"}, 404)