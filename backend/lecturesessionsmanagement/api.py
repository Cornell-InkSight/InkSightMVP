from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LectureSession, RecordingSession
from .serializers import LectureSessionSerializer, RecordingSessionSerializer
from django.shortcuts import render

"""
GET (LectureSession Management) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""
@api_view(["GET"])
def get_lecture_sessions(request):
    """Method to Fetch Courses"""
    lecture_sessions = LectureSession.objects.all()
    serializer = LectureSessionSerializer(lecture_sessions, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_lecture_session(request, lecture_session_id):
    """Method to Fetch Course"""
    try:
        course = LectureSession.objects.get(lecture_session_id)
        serializer = LectureSessionSerializer(course)
        return Response(serializer.data)
    except LectureSession.DoesNotExist:
        return Response({"error": "Course Does Not Exist in Database"}, 404)

@api_view(["GET"])
def get_recording_sessions(request):
    """Method to Fetch Courses"""
    recording_sessions = RecordingSession.objects.all()
    serializer = RecordingSessionSerializer(recording_sessions, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_recording_session(request, recording_session_id):
    """Method to Fetch Course"""
    try:
        course = RecordingSession.objects.get(recording_session_id)
        serializer = RecordingSessionSerializer(course)
        return Response(serializer.data)
    except RecordingSession.DoesNotExist:
        return Response({"error": "Course Does Not Exist in Database"}, 404)
    

"""
POST (Lecture Sessions) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_lecture_session(request):
    """Method to Add New Lecture Session"""
    lecture_session_data = request.data

    required_fields = ["date", "course", "notepacket", "status"]
    for field in required_fields:
        if field not in lecture_session_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    lecture_session = LectureSession.objects.create(
        date=lecture_session_data["date"], 
        course_id=lecture_session_data["course_id"], 
        notepacket = lecture_session_data["notepacket"],
        status = lecture_session_data["status"]
    )

    serializer = LectureSessionSerializer(lecture_session)
    return Response(serializer.data, status=201)    

@api_view(['POST'])
def add_recording_session(request):
    """Method to Add New Recording Session"""
    recording_session_data = request.data

    required_fields = ["lecture_session", "recording_type", "file_path", "created_at"]
    for field in required_fields:
        if field not in recording_session_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    recording_session = RecordingSession.objects.create(
        lecture_session_id=recording_session_data["lecture_session_id"], 
        recording_type=recording_session_data["recording_type"], 
        file_path = recording_session_data["file_path"],
        created_at = recording_session_data["created_at"]
    )

    serializer = RecordingSessionSerializer(recording_session)
    return Response(serializer.data, status=201)    