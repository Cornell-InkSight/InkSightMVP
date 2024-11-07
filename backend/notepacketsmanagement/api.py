from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import NotesPacket
from .serializers import NotesPacketSerializer


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
    notes_packets = NotesPacket.objects.all()
    serializer = NotesPacketSerializer(notes_packets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_note_packet(request, note_packet_id):
    """Method to Get Notes Packet ID"""
    try:
        notes_packet = NotesPacket.objects.get(id=note_packet_id)
        serializer = NotesPacketSerializer(notes_packet)
        return Response(serializer.data)
    except NotesPacket.DoesNotExist:
        return Response({"error": "Notes Packet Note in Database"}, 404)
    

"""
POST (Notes Packet) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_notes_packet(request):
    """Method to Add New Notes Packet"""
    notes_packet_data = request.data

    required_fields = ["note", "student_course_id", "professor_id", "teacher_assistant_id"]
    for field in required_fields:
        if field not in notes_packet_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    notes_packet = NotesPacket.objects.create(
        note=notes_packet_data["note"], 
        student_course_id=notes_packet_data["student_course_id"], 
        professor_id = notes_packet_data["professor_id"],
        teacher_assistant_id = notes_packet_data["teacher_assistant_id"]
    )

    serializer = NotesPacketSerializer(notes_packet)
    return Response(serializer.data, status=201)    