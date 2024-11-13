import os
import django
import random
from django.core.management.base import BaseCommand
from faker import Faker

from usermanagement.models import Student, Professor, SDSCoordinator, TeacherAssistant
from schoolmanagement.models import School
from coursemanagement.models import Course, StudentCourse, ProfessorCourse

fake = Faker()

class Command(BaseCommand):
    help = "Generate fake data for schools, students, professors, SDS coordinators, TAs, and courses."

    def handle(self, *args, **kwargs):
        self.create_fake_data()

    def create_fake_school(self, num_schools=1):
        """Create fake schools."""
        schools = []
        for _ in range(num_schools):
            school = School.objects.create(
                name=f"{fake.company()} University",
                
            )
            schools.append(school)
        return schools

    def create_fake_professors(self, schools, num_professors=10):
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

    def create_fake_sds_coordinators(self, schools, num_sds=5):
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

    def create_fake_tas(self, schools, professors, num_tas=10):
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

    def create_fake_students(self, schools, sds_coordinators, num_students=50):
        """Create fake students associated with schools."""
        students = []
        for _ in range(num_students):
            student = Student.objects.create(
                name=fake.name(),
                school=random.choice(schools),
                year=random.randint(1, 4),
                disability=random.choice(["Hearing Impaired", "Vision Impaired", "Dyslexia"]),
                sds_coordinator = random.choice(sds_coordinators)
            )
            students.append(student)
        return students

    def create_fake_courses(self, schools, sds_coordinators, num_courses=20):
        """Create fake courses with assigned SDS coordinators."""
        courses = []
        for _ in range(num_courses):
            course = Course.objects.create(
                name=f"{fake.word().capitalize()} 101",
                school=random.choice(schools),
                sds_coordinator=random.choice(sds_coordinators)
            )
            courses.append(course)
        return courses

    def create_fake_data(self):
        """Combine Functions to Create Full Fake Dataaset"""
        schools = self.create_fake_school()

        # Create professors, SDS coordinators, TAs, and students
        professors = self.create_fake_professors(schools)
        sds_coordinators = self.create_fake_sds_coordinators(schools)
        tas = self.create_fake_tas(schools, professors)
        students = self.create_fake_students(schools, sds_coordinators)

        # Create courses and associate with students
        courses = self.create_fake_courses(schools, sds_coordinators)
        for student in students:
            student_courses = random.sample(courses, k=random.randint(1, 3))
            for course in student_courses:
                StudentCourse.objects.create(student=student, course=course)
        for professor in professors:
            professor_courses = random.sample(courses, k=random.randint(1, 3))
            for course in professor_courses:
                ProfessorCourse.objects.create(professor=professor, course=course)

        self.stdout.write(self.style.SUCCESS("Fake data created successfully!"))
