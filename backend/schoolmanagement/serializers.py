from rest_framework import serializers
from .models import School

class SchoolSerializer(serializers.Serializer):
    """Serializer For School"""
    class Meta:
        model = School
        fields = ['id', 'name']