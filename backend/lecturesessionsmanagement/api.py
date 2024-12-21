from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LectureSession, RecordingSession, LectureSlides
from .serializers import LectureSessionSerializer, RecordingSessionSerializer, LectureSlidesSerializer
from rest_framework import status
from django.conf import settings
from django.core.files.storage import default_storage
import boto3
import os

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

@api_view(["GET"])
def get_current_lecture_session_for_course(request, course_id):
    """
    Retrieve a specific lecture session by ID.
    Args:
        lecture_session_id (int): The ID of the lecture session to retrieve.
    Returns:
        JSON response containing lecture session data if found; otherwise, a 404 error.
    """
    try:
        lecture_sessions = LectureSession.objects.filter(course_id=course_id, status="recording").order_by('-date')

        if not lecture_sessions.exists():
            return Response({"error": "No ongoing lecture session for this course"}, status=404)
        
        latest_lecture_session = lecture_sessions.first()

        serializer = LectureSessionSerializer(latest_lecture_session)
        return Response(serializer.data)
    except LectureSession.DoesNotExist:
        return Response({"error": "Lecture Session does not exist in the database"}, status=404)


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
    required_fields = ["date", "course_id", "status", "call_id"]

    # Validate required fields
    for field in required_fields:
        if field not in lecture_session_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new LectureSession object
    lecture_session = LectureSession.objects.create(
        date=lecture_session_data["date"],
        course_id=lecture_session_data["course_id"],
        status=lecture_session_data["status"],
        call_id = lecture_session_data["call_id"]
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
        
@api_view(['POST'])
def upload_lecture_session_slides(request, course_id):
    """
    Updates the slides for the lecture session to AmazonS3
    Creates A Temporary File Path in Django Storage and S3k3y
    Args:
        course_id (int): the ID of the course for file naming purposes
    """
    bucket_name = "inksightslidestorage"
    try:
        if 'file' not in request.FILES:
                return Response({"error": "No file uploaded."}, status=400)

        uploaded_file = request.FILES['file']
        temp_file_path = default_storage.save(uploaded_file.name, uploaded_file)

        s3_key = f"uploads/{course_id}/{uploaded_file.name}"
        s3_client = settings.GETS3CLIENT()
        s3_client.upload_file(temp_file_path, bucket_name, s3_key)

        AWS_REGION = os.getenv("AWS_COGNITO_REGION")
        
        url_to_s3 = f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        os.remove(temp_file_path)

        slides, created = LectureSlides.objects.get_or_create(file_slides=url_to_s3)
        if(created):
            serializer = LectureSlidesSerializer(created)
        else:
            serializer = LectureSlidesSerializer(slides)
        return Response({"message": "Slides uploaded successfully!", "slides": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404

@api_view(['POST'])
def set_lecture_session_for_slides(request, slides_id, lecture_session_id):
    """
    Associate a LectureSlides instance with a LectureSession.
    Updates the `lecture_session` field of a `LectureSlides` object to 
    associate it with a specific `LectureSession`
    Args:
        slides_id (int): The ID of the LectureSlides instance to update.
        lecture_session_id (int): The ID of the LectureSession to associate with the LectureSlides.
    Returns:
        Response: A JSON response with a success message or an error message.
    """
    try:
        # Retrieve the LectureSlides instance
        slides = LectureSlides.objects.get(id=slides_id)

        # Update the lecture_session field
        slides.lecture_session_id = lecture_session_id
        slides.save()

        # Return a success response
        return Response({"message": "Lecture session associated successfully."}, status=200)

    except LectureSlides.DoesNotExist:
        # Handle case where the slides ID does not exist
        raise Http404(f"LectureSlides with id {slides_id} does not exist.")

    except Exception as e:
        # Handle unexpected errors
        return Response({"error": str(e)}, status=500)


