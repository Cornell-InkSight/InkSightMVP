from rest_framework import serializers
from .models import LectureSession, RecordingSession, LectureSlides

class LectureSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureSession
        fields = ['id', 'date', 'course', 'status', 'call_id', 'title']

class RecordingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingSession
        fields = ['id', 'lecture_session', 'recording_type', 'file_path', 'created_at']

class LectureSlidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureSlides
        fields = ['id', 'file_slides', 'lecture_session_id']