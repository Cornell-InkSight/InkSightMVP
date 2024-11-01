from django.db import models
from coursemanagement.models import StudentCourse
from usermanagement.models import Professor, TeacherAssistant

class NotesPacket(models.Model):
    """Model for creating Notes Packet"""
    id = models.AutoField(primary_key=True)
    notes = models.JSONField(primary_key=True)
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    teahcher_assistant = models.ForeignKey(TeacherAssistant, on_delete=models.CASCADE)
    
