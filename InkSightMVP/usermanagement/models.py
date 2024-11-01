from django.db import models
from schoolmanagement.models import School

class Student(models.Model):
    """Model for adding student to database"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)
    year = models.IntegerField()
    disability = models.CharField(max_length=666)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Professor(models.Model):
    """Model for adding Professor to database"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TeacherAssistant(models.Model):
    """Model for adding Teacher Assistant to database"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)