from django.urls import path
from .api import *

urlpatterns = [
    path("students", get_students, name="get_students"),
    path("students/<int:student_id>", get_student, name="get_student"),
    path("students/add", add_student, name="add_student"),

    path("professors", get_professors, name="get_professors"),
    path("professors/<int:professor_id>", get_professor, name="get_professor"),
    path("professors/add", add_professor, name="add_professor"),

    path("tas", get_tas, name="get_tas"),
    path("tas/<int:ta_id>", get_ta, name="get_ta"),
    path("tas/add", add_ta, name="add_ta"),

    path("sdscoordinators", get_sdscoordinators, name="get_sdscoordinators"),
    path("sdscoordinators/<int:sds_coordinator_id>", get_sdscoordinator, name="get_sdscoordinator"),
    path("sdscoordinators/add", add_sds_coordinator, name="add_sds_coordinator"),
]