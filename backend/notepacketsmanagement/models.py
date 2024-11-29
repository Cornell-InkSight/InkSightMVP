from django.db import models
from coursemanagement.models import Course
from lecturesessionsmanagement.models import LectureSession
from usermanagement.models import Student

class NotesPacket(models.Model):
    """Model for creating Notes Packet"""
    id = models.AutoField(primary_key=True)
    notes = models.JSONField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    lecture_session = models.ForeignKey(LectureSession, on_delete=models.CASCADE, default=1)
    status = models.TextField(default="draft") # states can be draft, edits, approved
 
class StudentNotePacket(models.Model):
    """Model for creating Student Notes packet"""
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  
    lecture_session = models.ForeignKey(LectureSession, on_delete=models.CASCADE, default=1) 
    title = models.CharField(max_length=666, default="")
    time = models.DateTimeField()
    notes = models.JSONField(default=dict)