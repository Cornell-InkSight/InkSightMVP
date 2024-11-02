from django.contrib import admin
from .models import Student, Professor, TeacherAssistant, SDSCoordinator

admin.site.register(Professor)
admin.site.register(TeacherAssistant)
admin.site.register(Student)
admin.site.register(SDSCoordinator)