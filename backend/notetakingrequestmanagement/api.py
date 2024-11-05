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
def get_notes_packets():
    """Method to Get Notes Packets"""
    notes_packets = NoteTakingRequest.objects.all()
    serializer = NoteTakingRequestSerializer(notes_packets, many=True)
    return Response(serializer.data)

def get_note_packet(note_packet_id):
    """Method to Get Notes Packet ID"""
    try:
        notes_packet = NoteTakingRequest.objects.get(note_packet_id)
        serializer = NoteTakingRequestSerializer(notes_packet)
        return Response(serializer.data)
    except NoteTakingRequest.DoesNotExist:
        return Response({"error": "Notes Packet Note in Database"}, 404)