from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from usermanagement.models import User

class Permissions(models.Model):
    """Model for assigining permissions to user types"""
    id = models.AutoField(primary_key=True)

    # Defining Generic Foriegn Key (Student, 5) or (SDSCoordinator, 13)
    user_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_object_id = models.PositiveIntegerField()
    user = GenericForeignKey('user_content_type', 'user_object_id')

    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
                                      
    def __str__(self):
        return f"Permissions for {self.user_content_type} (ID: {self.user_object_id})"


