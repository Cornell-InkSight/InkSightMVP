from django.db import models
from coursemanagement.models import Course

class LectureSession(models.Model):
    """Model For Lecture Session"""
    id = models.AutoField(primary_key=True)
    title = models.TextField(default="Lecture")
    date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.TextField(default="recording")
    call_id = models.CharField(max_length=6, default="123456")

class RecordingSession(models.Model):
    """Model for Recording Session"""
    id = models.AutoField(primary_key=True)
    lecture_session = models.ForeignKey(LectureSession, on_delete=models.CASCADE)
    recording_type = models.TextField()
    file_path = models.CharField(max_length=2000)
    created_at = models.DateTimeField()