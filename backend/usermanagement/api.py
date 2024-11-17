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
    """
    Retrieve all student records.
    Fetches all student entries available in the database and returns them in JSON format.
    Returns:
        JSON response containing all student entries.
    """

    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_student(request, student_id):
    """
    Retrieve a specific student by ID.
    Args:
        student_id (int): The ID of the student to retrieve.
    Returns:
        JSON response containing student data if found; otherwise, a 404 error.
    """
    try:
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({"error": "Cannot locate student in database"}, 404)
    

@api_view(['GET'])
def get_sdscoordinators(request):
    """
    Retrieve all SDS Coordinator records.
    Fetches all SDS Coordinator entries available in the database and returns them in JSON format.
    Returns:
        JSON response containing all SDS Coordinator entries.
    """

    sdscoordinators = SDSCoordinator.objects.all()
    serializer = SDSCoordinatorSerializer(sdscoordinators, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_sdscoordinator(request, sds_coordinator_id):
    """
    Retrieve a specific SDS Coordinator by ID.
    Args:
        sds_coordinator_id (int): The ID of the SDS Coordinator to retrieve.
    Returns:
        JSON response containing SDS Coordinator data if found; otherwise, a 404 error.
    """

    try:
        sdscoordinator = SDSCoordinator.objects.get(id=sds_coordinator_id)
        serializer = SDSCoordinatorSerializer(sdscoordinator)
        return Response(serializer.data)
    except SDSCoordinator.DoesNotExist:
        return Response({"error": "SDS Coordinator Not in Database"}, 404)

@api_view(['GET'])
def get_professors(request):
    """
    Retrieve all professor records.
    Fetches all professor entries available in the database and returns them in JSON format.
    Returns:
        JSON response containing all professor entries.
    """

    professors = Professor.objects.all()
    serializer = ProfessorSerializer(professors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_professor(request, professor_id):
    """
    Retrieve a specific professor by ID.
    Args:
        professor_id (int): The ID of the professor to retrieve.
    Returns:
        JSON response containing professor data if found; otherwise, a 404 error.
    """

    try:
        professor = Professor.objects.get(id=professor_id)
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data)
    except Professor.DoesNotExist:
        return Response({"error": "Professor Is Not in Database"}, 404)

@api_view(['GET'])
def get_tas(request):
    """
    Retrieve all teaching assistant records.
    Fetches all teaching assistant entries available in the database and returns them in JSON format.
    Returns:
        JSON response containing all teaching assistant entries.
    """

    teacherassistants = TeacherAssistant.objects.all()
    serializer = TeacherAssistantSerializer(teacherassistants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_ta(request, ta_id):
    """
    Retrieve a specific teaching assistant by ID.
    Args:
        ta_id (int): The ID of the teaching assistant to retrieve.
    Returns:
        JSON response containing teaching assistant data if found; otherwise, a 404 error.
    """

    try:
        teacherassistant = TeacherAssistant.objects.get(id=ta_id)
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
    """
    Add a new student entry to the database.
    Expected JSON fields: name, school_id, year, disability.
    Args:
        request (Request): The HTTP request containing student data in JSON format.
    Returns:
        JSON response containing the created student data, or an error if validation fails.
    """

    student_data = request.data

    required_fields = ["name", "school_id", "year", "disability", "sds_coordinator_id"]
    for field in required_fields:
        if field not in student_data:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    
    student = Student.objects.create(
        name=student_data["name"], 
        school_id=student_data["school_id"], 
        year=student_data["year"], 
        disability=student_data["disability"],
        sds_coordinator_id = student_data["sds_coordinator_id"],
    )
    print(student)

    serializer = StudentSerializer(student)
    return Response(serializer.data, status=201)    

@api_view(['POST'])
def add_professor(request):
    """
    Add a new professor entry to the database.
    Expected JSON fields: name, school_id (optional: title with default "Dr.").
    Args:
        request (Request): The HTTP request containing professor data in JSON format.
    Returns:
        JSON response containing the created professor data, or an error if validation fails.
    """

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
    """
    Add a new teaching assistant (TA) entry to the database.
    Expected JSON fields: name, school_id, professor_id.
    Args:
        request (Request): The HTTP request containing TA data in JSON format.
    Returns:
        JSON response containing the created TA data, or an error if validation fails.
    """

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