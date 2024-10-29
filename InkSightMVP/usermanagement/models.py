from django.db import models
from schoolmanagement.models import School

class Student(models.Model):
    """Model for adding student to database"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)
    year = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Notetaker(models.Model):
    """Model for adding notetaker to database"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

