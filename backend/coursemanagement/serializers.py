from rest_framework import serializers
from .models import Course, StudentCourse, ProfessorCourse

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'school', 'sds_coordinator']

class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'student_id', 'course_id']

class ProfessorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorCourse
        fields = ['id', 'professor_id', 'course_id']