from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Permissions
from .serializers import PermissionsSerializer


"""
GET (Permissions) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""

@api_view(['GET'])
def get_permissions():
    """Method to Get Notes Packets"""
    permissions = Permissions.objects.all()
    serializer = PermissionsSerializer(permissions, many=True)
    return Response(serializer.data)

def get_note_packet(note_packet_id):
    """Method to Get Notes Packet ID"""
    try:
        permission = Permissions.objects.get(note_packet_id)
        serializer = PermissionsSerializer(permission)
        return Response(serializer.data)
    except Permissions.DoesNotExist:
        return Response({"error": "Notes Packet Note in Database"}, 404)
    
"""
POST (Permssions) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_permissions(request):
    """Method to Add New Notes Packet"""
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