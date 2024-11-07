from django.urls import path
from .api import *

urlpatterns = [
    path("students", get_students, name="get_students"),
    path("students/<int:student_id>", get_student, name="get_student"),

    path("professors", get_professors, name="get_professors"),
    path("professors/<int:professor_id>", get_professor, name="get_professor"),

    path("tas", get_tas, name="get_tas"),
    path("tas/<int:ta_id>", get_ta, name="get_ta"),

    path("sdscoordinators", get_sdscoordinators, name="get_sdscoordinators"),
    path("sdscoordinators/<int:sds_coordinator_id>", get_sdscoordinator, name="get_sdscoordinator"),
]