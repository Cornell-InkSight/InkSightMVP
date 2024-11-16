from django.db import models
from schoolmanagement.models import School
from usermanagement.models import Student, SDSCoordinator, Professor

class Course(models.Model):
    """Model for creating a course in a school"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    sds_coordinator = models.ForeignKey(SDSCoordinator, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " @ " + self.school.name

class StudentCourse(models.Model):
    """intermediary Model for connecting Students and Courses"""
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Student: {self.student.id}, Course: {self.course.id}"

class ProfessorCourse(models.Model):
    """intermediary Model for connecting Students and Courses"""
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Professor: {self.professor.id}, Course: {self.course.id}"
