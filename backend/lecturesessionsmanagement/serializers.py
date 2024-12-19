from rest_framework import serializers
from .models import LectureSession, RecordingSession

class LectureSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureSession
        fields = ['id', 'date', 'course', 'status', 'call_id', 'title']

class RecordingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingSession
        fields = ['id', 'lecture_session', 'recording_type', 'file_path', 'created_at']