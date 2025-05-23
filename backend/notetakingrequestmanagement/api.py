from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import NoteTakingRequest
from coursemanagement.models import StudentCourse
from usermanagement.models import Student
from usermanagement.serializers import StudentSerializer
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
def get_note_taking_requests(request):
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
def get_note_taking_request(request, note_taking_request_id):
    """
    Retrieve a specific note-taking request by ID.
    Args:
        note_taking_request_id (int): The ID of the note-taking request to retrieve.
    Returns:
        JSON response containing note-taking request data if found; otherwise, a 404 error.
    """
    try:
        notes_packet = NoteTakingRequest.objects.get(id=note_taking_request_id)
        serializer = NoteTakingRequestSerializer(notes_packet)
        return Response(serializer.data)
    except NoteTakingRequest.DoesNotExist:
        return Response({"error": "Note-taking request not found in database"}, status=404)
    
@api_view(['GET'])
def get_note_taking_request_request_for_course(request, course_id):
    """
    Retrieve the note-taking packets for specific course id
    Args:
        course_id (int): The ID of the course to retrieve note-taking packets
    Returns:
        JSON response containing note-taking request data for course if found; otherwise, a 404 error
    """
    try:
        notes_packets = NoteTakingRequest.objects.filter(student_course__course_id=course_id)
        serializer = NoteTakingRequestSerializer(notes_packets, many=True)
        return Response(serializer.data)
    except NoteTakingRequest.DoesNotExist:
        return Response({"error": "Note-taking request not found in database"}, status=404)
    
@api_view(['GET'])
def get_approved_students_for_notetaking_packets_for_course(request, course_id):
    """
    Retrieve all approved students who can receive note packets for a specific course.
    Args:
        course_id (int): The ID of the course to retrieve note-taking packets.
    Returns:
        JSON response containing student data for approved note-taking requests in the course if found; otherwise, a 404 error.
    """
    try:
        student_courses = StudentCourse.objects.filter(course_id=course_id)
        approved_requests = NoteTakingRequest.objects.filter(student_course__in=student_courses, approved=True)

        approved_student_ids = approved_requests.values_list('student_course__student_id', flat=True).distinct()
        approved_students = Student.objects.filter(id__in=approved_student_ids)
        serializer = StudentSerializer(approved_students, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=404)
    
@api_view(['GET'])
def get_student_notetaking_request_for_course(request, student_id, course_id):
    """
    Retrieve whether the student is approved for a specific course by ID
    Args:
        student_id (int): The ID of the student to retrieve note packets for.
        course_id (int): The ID of the course to retrieve note packets for.
    Returns:
        Boolean response if the student is approved or a message indicating no requests found.
    """
    try:
        student_course = StudentCourse.objects.get(course_id=course_id, student_id=student_id)
        
        note_taking_request = NoteTakingRequest.objects.filter(student_course_id=student_course).first()
        
        # Check if an approval request exists
        if note_taking_request:
            serializer = NoteTakingRequestSerializer(note_taking_request)
            return Response(serializer.data)
        else:
            return Response({ "error": "This student-course does not have an approval request."})
            
    except StudentCourse.DoesNotExist:
        return Response({"error": "Student is not enrolled in this course."}, status=404)

@api_view(['GET'])
def get_is_student_approved_for_course(request, student_id, course_id):
    """
    Retrieve whether the student is approved for a specific course by ID
    Args:
        student_id (int): The ID of the student to retrieve note packets for.
        course_id (int): The ID of the course to retrieve note packets for.
    Returns:
        Boolean response if the student is approved or a message indicating no requests found.
    """
    try:
        student_course = StudentCourse.objects.get(course_id=course_id, student_id=student_id)
        
        note_taking_request = NoteTakingRequest.objects.filter(student_course_id=student_course).first()
        
        # Check if an approval request exists
        if note_taking_request:
            return Response({"approved": note_taking_request.approved, "message": "Note-taking request succesfully returned."})
        else:
            return Response({"approved": False, "message": "This student-course does not have an approval request."})
            
    except StudentCourse.DoesNotExist:
        return Response({"error": "Student is not enrolled in this course."}, status=404)
    
@api_view(['GET'])
def get_student_has_pending_notetaking_request_for_course(request, student_id, course_id):
    """
    Retrieve whether the student has a pending notetaking request for a specific course by ID
    Args:
        student_id (int): The ID of the student to retrieve note packets for.
        course_id (int): The ID of the course to retrieve note packets for.
    Returns:
        Boolean response if the student is approved or a message indicating no requests found.
    """
    try:
        student_course = StudentCourse.objects.get(course_id=course_id, student_id=student_id)
        
        note_taking_request = NoteTakingRequest.objects.filter(student_course_id=student_course).first()
        
        # Check if an approval request exists
        if note_taking_request:
            return Response({"pending": not note_taking_request.approved, "message": "Note-taking request succesfully returned."})
        else:
            return Response({"pending": False, "message": "This student-course does not have an approval request."})
            
    except StudentCourse.DoesNotExist:
        return Response({"error": "Student is not enrolled in this course."}, status=404)
    

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
    Expected JSON fields: request, student_id, course_id, sdscoordinator_id.
    """
    note_taking_request_data = request.data
    required_fields = ["request", "student_id", "course_id", "sdscoordinator_id"]

    for field in required_fields:
        if field not in note_taking_request_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student_course = StudentCourse.objects.get(
            student_id=note_taking_request_data["student_id"],
            course_id=note_taking_request_data["course_id"]
        )
    except StudentCourse.DoesNotExist:
        return Response({"error": "Invalid student or course ID"}, status=status.HTTP_400_BAD_REQUEST)

    note_taking_request = NoteTakingRequest.objects.create(
        request=note_taking_request_data["request"],
        student_course_id=student_course.id,
        sdscoordinator_id=note_taking_request_data["sdscoordinator_id"],
    )

    serializer = NoteTakingRequestSerializer(note_taking_request)
    return Response(serializer.data, status=201)
    

"""
PUT (Note Taking Request Methods)
"""
@api_view(['PUT'])
def approve_notetaking_request(request, notetaking_request_id):
    """
    Approve note taking request by updating 'approved' to true
    Args:
        notetaking_request_id (int): the ID of the notetaking request to be approved
    """
    try:
        notetaking_request = NoteTakingRequest.objects.get(id=notetaking_request_id)
        notetaking_request.approved = True
        notetaking_request.save()
        return Response({"message": "Note-taking request approved successfully."}, status=status.HTTP_200_OK)
    except NoteTakingRequest.DoesNotExist:
        return Response({"error": "Note-taking request not found."}, status=status.HTTP_404_NOT_FOUND)



    