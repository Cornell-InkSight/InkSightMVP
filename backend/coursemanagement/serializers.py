from rest_framework import serializers
from .models import Course, StudentCourse

class CourseSerializer(serializers.Serializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'school', 'sds_coordinator']

class StudentCourseSerializer(serializers.Serializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'student_id', 'course_id']