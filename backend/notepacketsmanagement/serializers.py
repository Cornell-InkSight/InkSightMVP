from rest_framework import serializers
from .models import NotesPacket, StudentNotePacket

class NotesPacketSerializer(serializers.ModelSerializer):
    """Serializer For NotesPacket"""
    class Meta:
        model = NotesPacket
        fields = ['id', 'notes', 'course_id', 'lecture_session_id', 'status']

class StudentNotePacketSerializer(serializers.ModelSerializer):
    """Serializer got StudentNotePacket"""
    class Meta:
        model = StudentNotePacket
        fields = ['id', 'student_id', 'lecture_session_id', 'title', 'time']