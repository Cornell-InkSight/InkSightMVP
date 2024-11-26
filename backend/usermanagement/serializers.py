"""Serializer Functions To Transform Queried Data from DB into Python Readable Dictionaries"""

from rest_framework import serializers
from .models import Student, SDSCoordinator, Professor, TeacherAssistant

class StudentSerializer(serializers.ModelSerializer):
    """Serializer For Student"""
    class Meta:
        model = Student
        fields = ['user_ptr_id', 'email', 'name', 'school_id', 'year', 'disability', 'sds_coordinator_id']

class SDSCoordinatorSerializer(serializers.ModelSerializer):
    """Serializer for SDS Coordinator"""
    class Meta:
        model = SDSCoordinator
        fields = ['user_ptr_id', 'email', 'name', 'school_id', 'position', 'access_code']

class ProfessorSerializer(serializers.ModelSerializer):
    """Serializer For Professor"""
    class Meta:
        model = Professor
        fields = ['user_ptr_id', 'email', 'name', 'school_id', 'title']

class TeacherAssistantSerializer(serializers.ModelSerializer):
    """Serializer For TA"""
    class Meta:
        model = TeacherAssistant
        fields = ['user_ptr_id', 'email', 'name', 'school_id', 'professor_id']