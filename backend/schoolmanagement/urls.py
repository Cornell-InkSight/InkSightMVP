from django.urls import path
from .api import *

urlpatterns = [
    path("schools/", get_schools, name="get_schools"),
    path("schools/<int:school_id>", get_school, name="get_school"),
    path("schools/<int:school_id>/professors", get_professors_in_school, name="get_professors_in_school"),
    path("schools/add", add_school, name="add_school"),
    path("schools/<int:school_id>/courses", get_all_courses_for_school, name="get_all_courses_for_school")
]