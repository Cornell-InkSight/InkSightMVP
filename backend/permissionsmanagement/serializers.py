from rest_framework import serializers
from .models import Permissions
from django.contrib.contenttypes.models import ContentType

class PermissionsSerializer(serializers.ModelSerializer):
    user_content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model'
    )
    user_object_id = serializers.IntegerField()

    class Meta:
        model = Permissions
        fields = [
            'id', 'user_content_type', 'user_object_id', 'can_view', 'can_edit',
            'can_approve', 'submit_request', 'grant_recording_access', 'record_content',
            'convert_content', 'edit_notes', 'proofread_notes', 'access_digital_twin',
            'access_prof_portal', 'access_sds_portal', 'download_notes'
        ]
