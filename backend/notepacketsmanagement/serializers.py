from rest_framework import serializers
from .models import NotesPacket

class NotesPacketSerializer(serializers.Serializer):
    """Serializer For NotesPacket"""
    class Meta:
        model = NotesPacket
        fields = ['id', 'notes', 'student_course_id', 'professor_id', 'teacher_assistant_id']