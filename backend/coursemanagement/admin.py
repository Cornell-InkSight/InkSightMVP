from django.contrib import admin
from .models import Course, StudentCourse, ProfessorCourse

admin.site.register(Course)
admin.site.register(StudentCourse)
admin.site.register(ProfessorCourse)

