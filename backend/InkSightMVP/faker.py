import os
import django
from faker import Faker
import random

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InkSightMVP.settings")
django.setup()

from usermanagement.models import Student, Professor, SDSCoordinator, TeacherAssistant, User
from schoolmanagement.models import School
from coursemanagement.models import Course

fake = Faker()

def create_fake_school(num_schools=5):
    """Create fake schools."""
    schools = []
    for _ in range(num_schools):
        school = School.objects.create(
            name=f"{fake.company()} University",
            address=fake.address()
        )
        schools.append(school)
    return schools

def create_fake_professors(schools, num_professors=10):
    """Create fake professors associated with schools."""
    professors = []
    for _ in range(num_professors):
        professor = Professor.objects.create(
            name=fake.name(),
            school=random.choice(schools),
            title="Dr."
        )
        professors.append(professor)
    return professors

def create_fake_sds_coordinators(schools, num_sds=5):
    """Create fake SDS coordinators associated with schools."""
    sds_coordinators = []
    for _ in range(num_sds):
        sds_coordinator = SDSCoordinator.objects.create(
            name=fake.name(),
            school=random.choice(schools),
            position="SDS Coordinator"
        )
        sds_coordinators.append(sds_coordinator)
    return sds_coordinators

def create_fake_tas(schools, professors, num_tas=10):
    """Create fake TAs assigned to professors in schools."""
    tas = []
    for _ in range(num_tas):
        ta = TeacherAssistant.objects.create(
            name=fake.name(),
            school=random.choice(schools),
            professor=random.choice(professors)
        )
        tas.append(ta)
    return tas

def create_fake_students(schools, num_students=50):
    """Create fake students associated with schools."""
    students = []
    for _ in range(num_students):
        student = Student.objects.create(
            name=fake.name(),
            school=random.choice(schools),
            year=random.randint(1, 4),
            disability=random.choice(["None", "Hearing Impaired", "Vision Impaired", "Dyslexia"])
        )
        students.append(student)
    return students

def create_fake_courses(schools, professors, sds_coordinators, num_courses=20):
    """Create fake courses with assigned professors and SDS coordinators."""
    courses = []
    for _ in range(num_courses):
        course = Course.objects.create(
            name=f"{fake.word().capitalize()} 101",
            school=random.choice(schools),
            professor=random.choice(professors),
            sds_coordinator=random.choice(sds_coordinators)
        )
        courses.append(course)
    return courses

def create_fake_data():
    # Create schools
    schools = create_fake_school()
    
    # Create professors, SDS coordinators, TAs, and students
    professors = create_fake_professors(schools)
    sds_coordinators = create_fake_sds_coordinators(schools)
    tas = create_fake_tas(schools, professors)
    students = create_fake_students(schools)
    
    # Create courses and associate with students
    courses = create_fake_courses(schools, professors, sds_coordinators)
    for student in students:
        student_courses = random.sample(courses, k=random.randint(1, 3))
        for course in student_courses:
            StudentCourse.objects.create(student=student, course=course)

    print("Fake data created successfully!")

if __name__ == "__main__":
    create_fake_data()
