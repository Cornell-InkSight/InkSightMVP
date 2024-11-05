from django.urls import path
from .api import *

urlpatterns = [
    # Course GET methods
    path("courses/", get_courses, name="get_courses"),
    path("courses/<int:course_id>/", get_course, name="get_course"),
    
    # StudentCourse GET methods
    path("student-courses/", get_student_courses, name="get_student_courses"),
    path("student-courses/<int:student_id>/<int:course_id>/", get_student_course, name="get_student_course"),
    
    # Specific User-Course Relations GET methods
    path("students/<int:student_id>/courses/", get_all_courses_for_student, name="get_all_courses_for_student"),
    path("professors/<int:professor_id>/students/", get_all_students_for_professor, name="get_all_students_for_professor"),
    path("sds-coordinators/<int:sds_coordinator_id>/students/", get_all_students_for_sds_coordinator, name="get_all_students_for_sds_coordinator"),
    
    # Course POST methods
    path("courses/add/", add_course, name="add_course"),
    path("student-courses/add/", add_student_course, name="add_student_course"),
    path("students/<int:student_id>/courses/add/", add_course_for_student, name="add_course_for_student"),
]
