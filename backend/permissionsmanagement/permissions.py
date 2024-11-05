from django.contrib.contenttypes.models import ContentType
from usermanagement.models import Student, Professor, TeacherAssistant, SDSCoordinator
from .models import Permissions

def assign_student_permissions(student_instance, **kwargs):
    """
    Assign permissions to a Student instance.
    """
    student_content_type = ContentType.objects.get_for_model(Student)
    Permissions.objects.create(
        user_content_type=student_content_type,
        user_object_id=student_instance.id,
        can_view=kwargs.get("can_view", True),
        submit_request=kwargs.get("submit_request", True),
        record_content=kwargs.get("record_content", True),
        convert_content=kwargs.get("convert_content", True),
        download_notes=kwargs.get("download_notes", True),
        can_edit=kwargs.get("can_edit", False),
        can_approve=kwargs.get("can_approve", False)
    )

def assign_professor_permissions(professor_instance, **kwargs):
    """
    Assign permissions to a Professor instance.
    """
    professor_content_type = ContentType.objects.get_for_model(Professor)
    Permissions.objects.create(
        user_content_type=professor_content_type,
        user_object_id=professor_instance.id,
        can_view=kwargs.get("can_view", True),
        can_edit=kwargs.get("can_edit", True),
        can_approve=kwargs.get("can_approve", True),
        grant_recording_access=kwargs.get("grant_recording_access", True),
        record_content=kwargs.get("record_content", True),
        edit_notes=kwargs.get("edit_notes", True),
        proofread_notes=kwargs.get("proofread_notes", True),
        access_prof_portal=kwargs.get("access_prof_portal", True),
        access_digital_twin=kwargs.get("access_digital_twin", True)
    )

def assign_teacher_assistant_permissions(ta_instance, **kwargs):
    """
    Assign permissions to a Teacher Assistant instance.
    """
    ta_content_type = ContentType.objects.get_for_model(TeacherAssistant)
    Permissions.objects.create(
        user_content_type=ta_content_type,
        user_object_id=ta_instance.id,
        can_view=kwargs.get("can_view", True),
        can_edit=kwargs.get("can_edit", True),
        can_approve=kwargs.get("can_approve", False),
        proofread_notes=kwargs.get("proofread_notes", True),
        access_prof_portal=kwargs.get("access_prof_portal", True)
    )

def assign_sds_coordinator_permissions(sdscoordinator_instance, **kwargs):
    """
    Assign permissions to an SDS Coordinator instance.
    """
    sds_content_type = ContentType.objects.get_for_model(SDSCoordinator)
    Permissions.objects.create(
        user_content_type=sds_content_type,
        user_object_id=sdscoordinator_instance.id,
        can_view=kwargs.get("can_view", True),
        can_edit=kwargs.get("can_edit", True),
        can_approve=kwargs.get("can_approve", True),
        grant_recording_access=kwargs.get("grant_recording_access", True),
        access_sds_portal=kwargs.get("access_sds_portal", True)
    )


def assign_all_permissions():
    """Assigns default permissions for every user in the database."""
    for student in Student.objects.all():
        assign_student_permissions(student)

    for professor in Professor.objects.all():
        assign_professor_permissions(professor)

    for ta in TeacherAssistant.objects.all():
        assign_teacher_assistant_permissions(ta)

    for sdscoordinator in SDSCoordinator.objects.all():
        assign_sds_coordinator_permissions(sdscoordinator)

