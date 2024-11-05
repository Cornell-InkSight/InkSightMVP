from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import School
from .serializers import SchoolSerializer


"""
GET (Note Packets Management) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""

@api_view(['GET'])
def get_schools():
    """Method to Get Notes Packets"""
    schools = School.objects.all()
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)

def get_school(school_id):
    """Method to Get Notes Packet ID"""
    try:
        school = School.objects.get(school_id)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)
    except School.DoesNotExist:
        return Response({"error": "Notes Packet Note in Database"}, 404)
    
