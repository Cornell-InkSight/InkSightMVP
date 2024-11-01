from django.db import models
from coursemanagement.models import Course
from notepacketsmanagement.models import NotesPacket

class LectureSession(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    notepacket = models.ForeignKey(NotesPacket, on_delete=models.CASCADE)
    status = models.TextField()

class RecordingSession(models.Model):
    id = models.AutoField(primary_key=True)
    lecture_session = models.ForeignKey(LectureSession, on_delete=models.CASCADE)
    recording_type = models.TextField()
    file_path = models.CharField(max_length=2000)
    created_at = models.DateTimeField()