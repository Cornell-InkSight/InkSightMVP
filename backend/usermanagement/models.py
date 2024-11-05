from django.db import models
from schoolmanagement.models import School

class User(models.Model):
    """Generic User Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Student(User):
    """Model for adding student to database"""
    
    year = models.IntegerField()
    disability = models.CharField(max_length=666)

    


class Professor(User):
    """Model for adding Professor to database"""
    title = models.CharField(max_length=666)
    

class TeacherAssistant(User):
    """Model for adding Teacher Assistant to database"""
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)


class SDSCoordinator(User):
    """Model for creating an SDS Coordinator"""
    position = models.CharField(max_length=666)    
    