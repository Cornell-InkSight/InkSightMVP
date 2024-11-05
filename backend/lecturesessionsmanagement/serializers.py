from rest_framework import serializers
from .models import LectureSession, RecordingSession

class LectureSessionSerializer(serializers.Serializer):
    class Meta:
        model = LectureSession
        fields = ['id', 'date', 'course', 'notepacket', 'status']

class RecordingSessionSerializer(serializers.Serializer):
    class Meta:
        model = RecordingSession
        fields = ['id', 'lecture_session', 'recording_type', 'file_path', 'created_at']