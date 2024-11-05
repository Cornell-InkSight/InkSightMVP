from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Student, SDSCoordinator, Professor, TeacherAssistant
from .serializers import StudentSerializer, SDSCoordinatorSerializer, ProfessorSerializer, TeacherAssistantSerializer
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

"""
GET (User) Methods
1. Uses ORMs to query database, translating SQL to Python
2. Serializes data to turn into native Python data type (dictionary in this case), for conversion to JSON
3. Returns the data as an HttpResponse object, in the format of JSON
4. For specific users (fetched using id), use try/catch to check if that specific id exists
"""
@api_view(['GET'])
def get_students():
    """Method to Fetch Student Objects"""
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_student(student_id):
    """Method to Fetch Student"""
    
    try:
        student = Student.objects.get(student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({"error": "Cannot locate student in database"}, 404)
    

@api_view(['GET'])
def get_sdscoordinators():
    """Method to Fetch SDS Coordinators"""
    sdscoordinators = SDSCoordinator.objects.all()
    serializer = SDSCoordinatorSerializer(sdscoordinators, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_sdscoordinator(sds_coordinator_id):
    """Method to Fetch SDS Coordinator"""
    try:
        sdscoordinator = SDSCoordinator.objects.get(sds_coordinator_id)
        serializer = SDSCoordinatorSerializer(sdscoordinator)
        return Response(serializer.data)
    except SDSCoordinator.DoesNotExist:
        return Response({"error": "SDS Coordinator Not in Database"}, 404)

@api_view(['GET'])
def get_professors():
    """Method to Fetch Professors"""
    professors = Professor.objects.all()
    serializer = ProfessorSerializer(professors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_professor(professor_id):
    """Method to Fetch Professor"""
    try:
        professor = Professor.objects.get(professor_id)
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data)
    except Professor.DoesNotExist:
        return Response({"error": "Professor Is Not in Database"}, 404)

@api_view(['GET'])
def get_tas():
    """Method to Fetch TAs"""
    teacherassistants = TeacherAssistant.objects.all()
    serializer = TeacherAssistantSerializer(teacherassistants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_ta(ta_id):
    """Method to Fetch TA"""
    try:
        teacherassistant = TeacherAssistant.objects.get(ta_id)
        serializer = TeacherAssistantSerializer(teacherassistant)
        return Response(serializer.data)
    except TeacherAssistant.DoesNotExist:
        return Response({"error": "The TA Does not Exist in the Database"}, 404)