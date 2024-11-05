from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
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
def get_students(request):
    """Method to Fetch Student Objects"""
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_student(request, student_id):
    """Method to Fetch Student"""
    
    try:
        student = Student.objects.get(student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({"error": "Cannot locate student in database"}, 404)
    

@api_view(['GET'])
def get_sdscoordinators(request):
    """Method to Fetch SDS Coordinators"""
    sdscoordinators = SDSCoordinator.objects.all()
    serializer = SDSCoordinatorSerializer(sdscoordinators, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_sdscoordinator(request, sds_coordinator_id):
    """Method to Fetch SDS Coordinator"""
    try:
        sdscoordinator = SDSCoordinator.objects.get(sds_coordinator_id)
        serializer = SDSCoordinatorSerializer(sdscoordinator)
        return Response(serializer.data)
    except SDSCoordinator.DoesNotExist:
        return Response({"error": "SDS Coordinator Not in Database"}, 404)

@api_view(['GET'])
def get_professors(request):
    """Method to Fetch Professors"""
    professors = Professor.objects.all()
    serializer = ProfessorSerializer(professors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_professor(request, professor_id):
    """Method to Fetch Professor"""
    try:
        professor = Professor.objects.get(professor_id)
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data)
    except Professor.DoesNotExist:
        return Response({"error": "Professor Is Not in Database"}, 404)

@api_view(['GET'])
def get_tas(request):
    """Method to Fetch TAs"""
    teacherassistants = TeacherAssistant.objects.all()
    serializer = TeacherAssistantSerializer(teacherassistants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_ta(request, ta_id):
    """Method to Fetch TA"""
    try:
        teacherassistant = TeacherAssistant.objects.get(ta_id)
        serializer = TeacherAssistantSerializer(teacherassistant)
        return Response(serializer.data)
    except TeacherAssistant.DoesNotExist:
        return Response({"error": "The TA Does not Exist in the Database"}, 404)


"""
POST (User) Methods
1. Get the request data from the server (JSON)
2. List required fields and make sure the request has all necessary data, if not redo
3. create a new Object with all the fields, serialize and return
"""
@api_view(['POST'])
def add_student(request):
    """Method to Add New Student"""
    student_data = request.data

    required_fields = ["name", "school_id", "year", "disability"]
    for field in required_fields:
        if field not in student_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    student = Student.objects.create(
        name=student_data["name"], 
        school_id=student_data["school_id"], 
        year=student_data["year"], 
        disability=student_data["disability"]
    )

    serializer = StudentSerializer(student)
    return Response(serializer.data, status=201)    

@api_view(['POST'])
def add_professor(request):
    """Method to Add New Professor"""
    professor_data = request.data

    required_fields = ["name", "school_id"]
    for field in required_fields:
        if field not in professor_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    professor = Professor.objects.create(
        name=professor_data["name"], 
        school_id=professor_data["school_id"], 
        title=professor_data.get("title", "Dr.")
    )

    serializer = ProfessorSerializer(professor)
    return Response(serializer.data, status=201)    

@api_view(['POST'])
def add_ta(request):
    """Method to Add New TA"""
    ta_data = request.data

    required_fields = ["name", "school_id", "professor_id"]
    for field in required_fields:
        if field not in ta_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    ta = TeacherAssistant.objects.create(
        name=ta_data["name"], 
        school_id=ta_data["school_id"], 
        professor_id = ta_data["professor_id"]
    )

    serializer = TeacherAssistantSerializer(ta)
    return Response(serializer.data, status=201)    

@api_view(['POST'])
def add_sds_coordinator(request):
    """Method to Add New SDS Coordinator"""
    sds_coordinator_data = request.data

    required_fields = ["name", "school_id", "position"]
    for field in required_fields:
        if field not in sds_coordinator_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)


    sds_coordinator = SDSCoordinator.objects.create(
        name=sds_coordinator_data["name"], 
        school_id=sds_coordinator_data["school_id"], 
        position=sds_coordinator_data["position"], 
    )

    serializer = SDSCoordinatorSerializer(sds_coordinator)
    return Response(serializer.data, status=201)    