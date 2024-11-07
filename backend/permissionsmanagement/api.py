from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Permissions
from .serializers import PermissionsSerializer
from django.contrib.contenttypes.models import ContentType
from usermanagement.models import Student, Professor, TeacherAssistant, SDSCoordinator

"""
GET (Permissions) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""

@api_view(['GET'])
def get_permissions(request):
    """
    Retrieve all permissions.
    Fetches all permission entries available in the database and returns them in JSON format.
    Returns:
        JSON response containing all permissions.
    """
    permissions = Permissions.objects.all()
    serializer = PermissionsSerializer(permissions, many=True)
    return Response(serializer.data)

def get_note_packet(request, permission_id):
    """
    Retrieve a specific permission entry by ID.
    Args:
        permission_id (int): The ID of the permission entry to retrieve.
    Returns:
        JSON response containing permission data if found; otherwise, a 404 error.
    """
    try:
        permission = Permissions.objects.get(id=permission_id)
        serializer = PermissionsSerializer(permission)
        return Response(serializer.data)
    except Permissions.DoesNotExist:
        return Response({"error": "Permissions Not in Database"}, 404)
    
"""
POST (Permssions) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_permissions(request):
    """
    Add a new permission entry to the database.
    Expected JSON fields: request, student_course_id, sdscoordinator_id.
    Args:
        request (Request): The HTTP request containing permission data in JSON format.
    Returns:
        JSON response containing the created permission data, or an error if validation fails.
    """
    permissions_data = request.data

    required_fields = ["request", "student_course_id", "sdscoordinator_id"]
    for field in required_fields:
        if field not in permissions_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    permissions = Permissions.objects.create(
        request=permissions_data["request"], 
        student_course_id=permissions_data["student_course_id"], 
        sdscoordinator_id = permissions_data["sdscoordinator_id"],
    )

    serializer = PermissionsSerializer(permissions)
    return Response(serializer.data, status=201)    


"""
POST (Permissions) Methods specialized
"""
def assign_student_permissions(student_instance, **kwargs):
    """
    Assign permissions to a Student instance.
    Args:
        student_instance (Student): The student instance to which permissions are assigned.
        kwargs: Additional permission attributes as keyword arguments.
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
    Args:
        professor_instance (Professor): The professor instance to which permissions are assigned.
        kwargs: Additional permission attributes as keyword arguments.
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
    Args:
        ta_instance (TeacherAssistant): The teacher assistant instance to which permissions are assigned.
        kwargs: Additional permission attributes as keyword arguments.
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
    Args:
        sdscoordinator_instance (SDSCoordinator): The SDS Coordinator instance to which permissions are assigned.
        kwargs: Additional permission attributes as keyword arguments.
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
    """
    Assigns default permissions for every user in the database.
    Loops through all instances of Student, Professor, Teacher Assistant, and SDS Coordinator models,
    assigning the default permissions to each based on their role.
    """

    for student in Student.objects.all():
        assign_student_permissions(student)

    for professor in Professor.objects.all():
        assign_professor_permissions(professor)

    for ta in TeacherAssistant.objects.all():
        assign_teacher_assistant_permissions(ta)

    for sdscoordinator in SDSCoordinator.objects.all():
        assign_sds_coordinator_permissions(sdscoordinator)

