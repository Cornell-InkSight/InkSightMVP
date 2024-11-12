from django.db import models
from coursemanagement.models import Course
from lecturesessionsmanagement.models import LectureSession

class NotesPacket(models.Model):
    """Model for creating Notes Packet"""
    id = models.AutoField(primary_key=True)
    notes = models.JSONField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    lecture_session = models.ForeignKey(LectureSession, on_delete=models.CASCADE, default=1)
    status = models.TextField(default="draft") # states can be draft, edits, approved
 