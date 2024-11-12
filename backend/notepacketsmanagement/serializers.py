from rest_framework import serializers
from .models import NotesPacket

class NotesPacketSerializer(serializers.ModelSerializer):
    """Serializer For NotesPacket"""
    class Meta:
        model = NotesPacket
        fields = ['id', 'notes', 'course_id', 'lecture_session_id', 'status']