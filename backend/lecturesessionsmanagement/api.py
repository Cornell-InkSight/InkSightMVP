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
def get_lecture_sessions():
    """Method to Fetch Courses"""
    lecture_sessions = LectureSession.objects.all()
    serializer = LectureSessionSerializer(lecture_sessions, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_lecture_session(lecture_session_id):
    """Method to Fetch Course"""
    try:
        course = LectureSession.objects.get(lecture_session_id)
        serializer = LectureSessionSerializer(course)
        return Response(serializer.data)
    except LectureSession.DoesNotExist:
        return Response({"error": "Course Does Not Exist in Database"}, 404)

@api_view(["GET"])
def get_recording_sessions():
    """Method to Fetch Courses"""
    recording_sessions = RecordingSession.objects.all()
    serializer = RecordingSessionSerializer(recording_sessions, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_recording_session(recording_session_id):
    """Method to Fetch Course"""
    try:
        course = RecordingSession.objects.get(recording_session_id)
        serializer = RecordingSessionSerializer(course)
        return Response(serializer.data)
    except RecordingSession.DoesNotExist:
        return Response({"error": "Course Does Not Exist in Database"}, 404)
    
