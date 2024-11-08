from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import School
from usermanagement.models import Professor
from coursemanagement.models import Course
from coursemanagement.serializers import CourseSerializer
from usermanagement.serializers import ProfessorSerializer
from .serializers import SchoolSerializer


"""
GET (School Management) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""

@api_view(['GET'])
def get_schools(request):
    """
    Retrieve all schools.
    Fetches all school entries available in the database and returns them in JSON format.
    Returns:
        JSON response containing all school entries.
    """
    schools = School.objects.all()
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_school(request, school_id):
    """
    Retrieve a specific school by ID.
    Args:
        school_id (int): The ID of the school to retrieve.
    Returns:
        JSON response containing school data if found; otherwise, a 404 error.
    """

    try:
        school = School.objects.get(id=school_id)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)
    except School.DoesNotExist:
        return Response({"error": "School Note in Database"}, 404)
    
@api_view(['GET'])
def get_professors_in_school(request, school_id):
    """
    Retrieve all professors associated with a specific school by school ID.
    Args:
        school_id (int): The ID of the school whose professors are to be retrieved.
    Returns:
        JSON response containing professor data if the school is found; otherwise, a 404 error.
    """

    try:
        professor = Professor.objects.filter(school_id=school_id)
        serializer = ProfessorSerializer(professor, many=True)
        return Response(serializer.data)
    except School.DoesNotExist:
        return Response({"error": "School Not in Database"}, 404)
    
@api_view(["GET"])
def get_all_courses_for_school(request, school_id):
    """
    Retrieve all courses associated with a specific school.
    Args:
        school_id (int): The ID of the school.
    Returns:
        JSON response containing courses associated with the school, or an error message.
    """
    courses = Course.objects.filter(school_id=school_id)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

"""
POST (School) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_school(request):
    """
    Add a new school entry to the database.
    Expected JSON fields: name.
    Args:
        request (Request): The HTTP request containing school data in JSON format.
    Returns:
        JSON response containing the created school data, or an error if validation fails.
    """

    school_data = request.data

    required_fields = ["name"]
    for field in required_fields:
        if field not in school_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    school = School.objects.create(
        name=school_data["name"], 
    )

    serializer = SchoolSerializer(school)
    return Response(serializer.data, status=201)    