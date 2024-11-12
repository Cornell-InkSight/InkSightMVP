from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LectureSession, RecordingSession
from .serializers import LectureSessionSerializer, RecordingSessionSerializer
from rest_framework import status

"""
GET (LectureSession Management) Methods
Provides methods for retrieving lecture sessions and recording sessions. Each method:
1. Uses Django ORM to query the database.
2. Serializes the data into a native Python data type (dictionary) for JSON conversion.
3. Returns the data as an HTTP response in JSON format.
4. Uses try-except blocks for fetching specific records by ID, returning a 404 error if not found.
"""

@api_view(["GET"])
def get_lecture_sessions(request):
    """
    Retrieve all lecture sessions.
    Fetches all lecture sessions available in the database and returns them in JSON format.
    Returns:
        JSON response containing all lecture sessions.
    """
    lecture_sessions = LectureSession.objects.all()
    serializer = LectureSessionSerializer(lecture_sessions, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_lecture_session(request, lecture_session_id):
    """
    Retrieve a specific lecture session by ID.
    Args:
        lecture_session_id (int): The ID of the lecture session to retrieve.
    Returns:
        JSON response containing lecture session data if found; otherwise, a 404 error.
    """
    try:
        lecture_session = LectureSession.objects.get(id=lecture_session_id)
        serializer = LectureSessionSerializer(lecture_session)
        return Response(serializer.data)
    except LectureSession.DoesNotExist:
        return Response({"error": "Lecture Session does not exist in the database"}, status=404)

@api_view(["GET"])
def get_recording_sessions(request):
    """
    Retrieve all recording sessions.
    Fetches all recording sessions available in the database and returns them in JSON format.
    Returns:
        JSON response containing all recording sessions.
    """
    recording_sessions = RecordingSession.objects.all()
    serializer = RecordingSessionSerializer(recording_sessions, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_recording_session(request, recording_session_id):
    """
    Retrieve a specific recording session by ID.
    Args:
        recording_session_id (int): The ID of the recording session to retrieve.
    Returns:
        JSON response containing recording session data if found; otherwise, a 404 error.
    """
    try:
        recording_session = RecordingSession.objects.get(id=recording_session_id)
        serializer = RecordingSessionSerializer(recording_session)
        return Response(serializer.data)
    except RecordingSession.DoesNotExist:
        return Response({"error": "Recording Session does not exist in the database"}, status=404)

"""
POST (Lecture Session and Recording Session) Methods
Handles the creation of new lecture sessions and recording sessions.
Each function:
1. Retrieves JSON data from the request.
2. Validates required fields to ensure all necessary data is present.
3. Creates the object, serializes it, and returns the created data in the response.
"""

@api_view(['POST'])
def add_lecture_session(request):
    """
    Add a new lecture session to the database.
    Expected JSON fields: date, course_id, status.
    Args:
        request (Request): The HTTP request containing lecture session data in JSON format.
    Returns:
        JSON response containing the created lecture session data, or an error if validation fails.
    """
    lecture_session_data = request.data
    required_fields = ["date", "course_id", "status"]

    # Validate required fields
    for field in required_fields:
        if field not in lecture_session_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new LectureSession object
    lecture_session = LectureSession.objects.create(
        date=lecture_session_data["date"],
        course_id=lecture_session_data["course_id"],
        status=lecture_session_data["status"]
    )

    serializer = LectureSessionSerializer(lecture_session)
    return Response(serializer.data, status=201)

@api_view(['POST'])
def add_recording_session(request):
    """
    Add a new recording session linked to a lecture session.
    Expected JSON fields: lecture_session_id, recording_type, file_path, created_at.
    Args:
        request (Request): The HTTP request containing recording session data in JSON format.
    Returns:
        JSON response containing the created recording session data, or an error if validation fails.
    """
    recording_session_data = request.data
    required_fields = ["lecture_session_id", "recording_type", "file_path", "created_at"]

    # Validate required fields
    for field in required_fields:
        if field not in recording_session_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new RecordingSession object
    recording_session = RecordingSession.objects.create(
        lecture_session_id=recording_session_data["lecture_session_id"],
        recording_type=recording_session_data["recording_type"],
        file_path=recording_session_data["file_path"],
        created_at=recording_session_data["created_at"]
    )

    serializer = RecordingSessionSerializer(recording_session)
    return Response(serializer.data, status=201)

@api_view(['PUT'])
def update_lecture_session_status(request, lecture_session_id):
    """
    Updates the status of the lecture session
    Args:
        lecture_session_id (int): The ID of the lecture session
        status (string): The status message to be updated
    """
    
    try:
        lecture_session = LectureSession.objects.get(id=lecture_session_id)
        lecture_status = request.data.get('status')
        lecture_session.status = lecture_status
        lecture_session.save()
        return Response({"message": "Lecture Session updated successfully."}, status=status.HTTP_200_OK)
    except LectureSession.DoesNotExist:
        return Response({"error": "Lecture Session not found."}, status=status.HTTP_404_NOT_FOUND)
        