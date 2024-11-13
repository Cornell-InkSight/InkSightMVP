from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import NotesPacket
from .serializers import NotesPacketSerializer

"""
GET (Notes Packet Management) Methods
Provides methods to retrieve Notes Packets data. Each method:
1. Uses Django ORM to query the database.
2. Serializes the data into a native Python type (dictionary) for JSON conversion.
3. Returns the data as an HTTP response in JSON format.
4. Uses try-except blocks to handle cases where specific entries are not found.
"""

@api_view(['GET'])
def get_notes_packets(request):
    """
    Retrieve all notes packets.
    Fetches all notes packets available in the database and returns them in JSON format.
    Returns:
        JSON response containing all notes packets.
    """
    notes_packets = NotesPacket.objects.all()
    serializer = NotesPacketSerializer(notes_packets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_note_packet(request, note_packet_id):
    """
    Retrieve a specific notes packet by ID.
    Args:
        note_packet_id (int): The ID of the notes packet to retrieve.
    Returns:
        JSON response containing notes packet data if found; otherwise, a 404 error.
    """
    try:
        notes_packet = NotesPacket.objects.get(id=note_packet_id)
        serializer = NotesPacketSerializer(notes_packet)
        return Response(serializer.data)
    except NotesPacket.DoesNotExist:
        return Response({"error": "Notes Packet not found in database"}, status=404)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_note_packets_for_course(request, course_id):
    """
    Retrieve notes packets for a specific course by ID.
    Args:
        course_id (int): The ID of the course to retrieve note packets for.
    Returns:
        JSON response containing notes packet data if found; otherwise, an empty list.
    """
    notes_packets = NotesPacket.objects.filter(course_id=course_id)
    serializer = NotesPacketSerializer(notes_packets, many=True)
    return Response(serializer.data) 


@api_view(['GET'])
def get_published_note_packets_for_course(request, course_id):
    """
    Retrieve published notes packets for a specific course by ID.
    Args:
        course_id (int): The ID of the course to retrieve note packets for.
    Returns:
        JSON response containing notes packet data if found; otherwise, an empty list.
    """
    published_packets = NotesPacket.objects.filter(course_id=course_id, status="published")
    serializer = NotesPacketSerializer(published_packets, many=True)
    return Response(serializer.data)  


@api_view(['GET'])
def get_unpublished_note_packets_for_course(request, course_id):
    """
    Retrieve unpublished notes packets for a specific course by ID.
    Args:
        course_id (int): The ID of the course to retrieve note packets for.
    Returns:
        JSON response containing notes packet data if found; otherwise, an empty list.
    """
    unpublished_packets = NotesPacket.objects.filter(course_id=course_id).exclude(status="published")
    serializer = NotesPacketSerializer(unpublished_packets, many=True)
    return Response(serializer.data)  


"""
POST (Notes Packet) Methods
Handles the creation of new Notes Packets. Each function:
1. Retrieves JSON data from the request.
2. Validates that all required fields are provided.
3. Creates the object, serializes it, and returns the created data in the response.
"""

@api_view(['POST'])
def add_notes_packet(request):
    """
    Add a new notes packet to the database.
    Expected JSON fields: note, course_id, lecture_session_id
    Args:
        request (Request): The HTTP request containing notes packet data in JSON format.
    Returns:
        JSON response containing the created notes packet data, or an error if validation fails.
    """
    notes_packet_data = request.data
    required_fields = ["notes", "course_id", "lecture_session_id"]

    # Validate required fields
    for field in required_fields:
        if field not in notes_packet_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new NotesPacket object
    notes_packet = NotesPacket.objects.create(
        notes=notes_packet_data["notes"],
        course_id=notes_packet_data["course_id"],
        lecture_session_id=notes_packet_data["lecture_session_id"],
    )

    serializer = NotesPacketSerializer(notes_packet)
    return Response(serializer.data, status=201)

@api_view(['POST'])
def update_notes_packet_status(request, note_packet_id):
    """
    Updates the status of the notes packet to the databse
    Args:
        Status to be updated in Notes Packet
    """    
    try:
        notes_packet_session = NotesPacket.objects.get(id=note_packet_id)
        notes_packet_status = request.data.get('status')
        notes_packet_session.status = notes_packet_status
        notes_packet_session.save()
        return Response({"message": "notes packet Session updated successfully."}, status=status.HTTP_200_OK)
    except NotesPacket.DoesNotExist:
        return Response({"error": "notes packet Session not found."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def update_notes_packet_text(request, note_packet_id):
    """
    Updates the text of the notes packet to the databse
    Args:
        text to be updated in Notes Packet
    """    
    try:
        notes_packet_session = NotesPacket.objects.get(id=note_packet_id)
        notes_packet_text = request.data.get('text')
        notes_packet_session.notes = notes_packet_text
        notes_packet_session.save()
        return Response({"message": "notes packet Session updated successfully."}, status=status.HTTP_200_OK)
    except NotesPacket.DoesNotExist:
        return Response({"error": "notes packet Session not found."}, status=status.HTTP_404_NOT_FOUND)