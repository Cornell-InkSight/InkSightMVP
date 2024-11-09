from rest_framework import serializers
from .models import NoteTakingRequest

class NoteTakingRequestSerializer(serializers.ModelSerializer):
    """Serializer For NoteTakingRequest"""
    class Meta:
        model = NoteTakingRequest
        fields = ['id', 'request', 'student_course_id', 'sdscoordinator_id']