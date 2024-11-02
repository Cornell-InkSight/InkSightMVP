from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from usermanagement.models import User

class Permissions(models.Model):
    """Model for assigning permissions to user types"""
    id = models.AutoField(primary_key=True)

    # Defining Generic Foreign Key (e.g., (Student, 5) or (SDSCoordinator, 13))
    user_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_object_id = models.PositiveIntegerField()
    user = GenericForeignKey('user_content_type', 'user_object_id')

    # Permissions
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    submit_request = models.BooleanField(default=False)
    grant_recording_access = models.BooleanField(default=False)
    record_content = models.BooleanField(default=False)
    convert_content = models.BooleanField(default=False)
    edit_notes = models.BooleanField(default=False)
    proofread_notes = models.BooleanField(default=False)
    access_digital_twin = models.BooleanField(default=False)
    access_prof_portal = models.BooleanField(default=False)
    access_sds_portal = models.BooleanField(default=False)
    download_notes = models.BooleanField(default=False)

    def __str__(self):
        return f"Permissions for {self.user_content_type} (ID: {self.user_object_id})"
