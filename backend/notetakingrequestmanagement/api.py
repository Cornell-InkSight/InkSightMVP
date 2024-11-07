from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import NoteTakingRequest
from .serializers import NoteTakingRequestSerializer


"""
GET (Note Packets Management) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""

@api_view(['GET'])
def get_notes_packets(request):
    """Method to Get Notes Packets"""
    notes_packets = NoteTakingRequest.objects.all()
    serializer = NoteTakingRequestSerializer(notes_packets, many=True)
    return Response(serializer.data)

def get_note_packet(request, note_packet_id):
    """Method to Get Notes Packet ID"""
    try:
        notes_packet = NoteTakingRequest.objects.get(id=note_packet_id)
        serializer = NoteTakingRequestSerializer(notes_packet)
        return Response(serializer.data)
    except NoteTakingRequest.DoesNotExist:
        return Response({"error": "Notes Packet Note in Database"}, 404)
    
"""
POST (Note Taking Request) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_note_taking_request(request):
    """Method to Add New Notes Packet"""
    note_taking_request_data = request.data

    required_fields = ["request", "student_course_id", "sdscoordinator_id"]
    for field in required_fields:
        if field not in note_taking_request_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    note_taking_request = NoteTakingRequest.objects.create(
        request=note_taking_request_data["request"], 
        student_course_id=note_taking_request_data["student_course_id"], 
        sdscoordinator_id = note_taking_request_data["sdscoordinator_id"],
    )

    serializer = NoteTakingRequestSerializer(note_taking_request)
    return Response(serializer.data, status=201)    