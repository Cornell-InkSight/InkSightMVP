from django.db import models
from coursemanagement.models import StudentCourse
from usermanagement.models import SDSCoordinator

class NoteTakingRequest(models.Model):
    """Model For Creating Notetaking Request"""
    id = models.AutoField(primary_key=True)
    request = models.TextField()
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    sdscoordinator = models.ForeignKey(SDSCoordinator, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request {self.id} for Course {self.course.name}"
     