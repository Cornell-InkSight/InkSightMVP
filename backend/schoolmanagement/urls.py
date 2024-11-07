from django.urls import path
from .api import *

urlpatterns = [
    path("schools/", get_schools, name="get_schools"),
    path("schools/<int:school_id>", get_school, name="get_school"),
    path("schools/professors/<int:school_id>", get_professors_in_school, name="get_professors_in_school"),
    path("schools/add", add_school, name="add_school")
]