from rest_framework import serializers
from .models import NoteTakingRequest

class NoteTakingRequestSerializer(serializers.Serializer):
    """Serializer For NoteTakingRequest"""
    class Meta:
        model = NoteTakingRequest
        fields = ['id', 'request', 'student_course_id', 'sds_coordinator_id']