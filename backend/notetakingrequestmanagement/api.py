from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import NoteTakingRequest
from .serializers import NoteTakingRequestSerializer

"""
GET (Note Taking Request Management) Methods
Provides methods to retrieve note-taking requests data. Each method:
1. Uses Django ORM to query the database.
2. Serializes the data into a native Python type (dictionary) for JSON conversion.
3. Returns the data as an HTTP response in JSON format.
4. Uses try-except blocks to handle cases where specific entries are not found.
"""

@api_view(['GET'])
def get_notes_packets(request):
    """
    Retrieve all note-taking requests.
    Fetches all note-taking requests available in the database and returns them in JSON format.
    Returns:
        JSON response containing all note-taking requests.
    """
    notes_packets = NoteTakingRequest.objects.all()
    serializer = NoteTakingRequestSerializer(notes_packets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_note_packet(request, note_packet_id):
    """
    Retrieve a specific note-taking request by ID.
    Args:
        note_packet_id (int): The ID of the note-taking request to retrieve.
    Returns:
        JSON response containing note-taking request data if found; otherwise, a 404 error.
    """
    try:
        notes_packet = NoteTakingRequest.objects.get(id=note_packet_id)
        serializer = NoteTakingRequestSerializer(notes_packet)
        return Response(serializer.data)
    except NoteTakingRequest.DoesNotExist:
        return Response({"error": "Note-taking request not found in database"}, status=404)
    
"""
POST (Note Taking Request) Methods
Handles the creation of new note-taking requests. Each function:
1. Retrieves JSON data from the request.
2. Validates that all required fields are provided.
3. Creates the object, serializes it, and returns the created data in the response.
"""

@api_view(['POST'])
def add_note_taking_request(request):
    """
    Add a new note-taking request to the database.
    Expected JSON fields: request, student_course_id, sdscoordinator_id.
    Args:
        request (Request): The HTTP request containing note-taking request data in JSON format.
    Returns:
        JSON response containing the created note-taking request data, or an error if validation fails.
    """
    note_taking_request_data = request.data
    required_fields = ["request", "student_course_id", "sdscoordinator_id"]

    # Validate required fields
    for field in required_fields:
        if field not in note_taking_request_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new NoteTakingRequest object
    note_taking_request = NoteTakingRequest.objects.create(
        request=note_taking_request_data["request"],
        student_course_id=note_taking_request_data["student_course_id"],
        sdscoordinator_id=note_taking_request_data["sdscoordinator_id"],
    )

    serializer = NoteTakingRequestSerializer(note_taking_request)
    return Response(serializer.data, status=201)
