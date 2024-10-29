from django.db import models


class School(models.Model):
    """Model for creating a school"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)

    def __str__(self):
        return self.name

class SDSCoordinator(models.Model):
    """Model for creating an SDS Coordinator"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=666)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name