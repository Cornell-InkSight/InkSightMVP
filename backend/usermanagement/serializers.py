"""Serializer Functions To Transform Queried Data from DB into Python Readable Dictionaries"""

from rest_framework import serializers
from .models import Student, SDSCoordinator, Professor, TeacherAssistant

class StudentSerializer(serializers.ModelSerializer):
    """Serializer For Student"""
    class Meta:
        model = Student
        fields = ['id', 'name', 'school', 'year', 'disability']

class SDSCoordinatorSerializer(serializers.ModelSerializer):
    """Serializer for SDS Coordinator"""
    class Meta:
        model = SDSCoordinator
        fields = ['id', 'name', 'school', 'position']

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'name', 'school', 'title']

class TeacherAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAssistant
        fields = ['id', 'name', 'school', 'professor_id']