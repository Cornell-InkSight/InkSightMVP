from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import School
from usermanagement.models import Professor
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
    """Method to School Packets"""
    schools = School.objects.all()
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_school(request, school_id):
    """Method to Get School ID"""
    try:
        school = School.objects.get(school_id)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)
    except School.DoesNotExist:
        return Response({"error": "School Note in Database"}, 404)
    
@api_view(['GET'])
def get_professors_in_school(request, school_id):
    try:
        school = School.objects.get(school_id)
        professor = Professor.objects.filter(school_id__in=school)
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data)
    except School.DoesNotExist:
        return Response({"error": "School Not in Database"}, 404)

"""
POST (School) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_school(request):
    """Method to Add New School Packet"""
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