from django.urls import path
from .api import *

urlpatterns = [
    # Course GET methods
    path("courses/", get_courses, name="get_courses"),
    path("courses/<int:course_id>/", get_course, name="get_course"),
    
    # StudentCourse GET methods
    path("student-courses/", get_student_courses, name="get_student_courses"),
    path("student-courses/<int:student_id>/<int:course_id>/", get_student_course, name="get_student_course"),
    path("student-courses/<int:studentcourse_id>", get_student_course_with_id, name="get_student_course_with_id"),
    
    # Specific User-Course Relations GET methods
    path("students/<int:student_id>/courses/", get_all_courses_for_student, name="get_all_courses_for_student"),
    path("professors/<int:professor_id>/students/", get_all_students_for_professor, name="get_all_students_for_professor"),
    path("professors/<int:course_id>", get_all_students_for_professor_for_course, name="get_all_students_for_professor_for_course"),
    path("professors/<int:professor_id>/courses/", get_all_courses_for_professor, name="get_all_courses_for_professor"),
    path("sdscoordinators/<int:sds_coordinator_id>/students/", get_all_students_for_sds_coordinator, 
    name="get_all_students_for_sds_coordinator"),
    path("courses/<int:course_id>/professors/", get_all_professors_for_courses, name="get_all_professors_for_courses"),
    path("courses/<int:course_id>/sdscoordinator", get_sds_coordinator_course, name="get_sds_coordinator_course"),
    path("tas/courses/<int:ta_id>", get_all_courses_for_ta, name="get_all_courses_for_ta"),
    path("courses/<int:professor_id>/<int:course_id>/tas", get_all_tas_for_courses, name="get_all_tas_for_courses"),
    
    # Course POST methods
    path("courses/add/", add_course, name="add_course"),
    path("student-courses/add/", add_student_course, name="add_student_course"),
    path("students/<int:student_id>/courses/add/", add_new_course_for_student, name="add_new_course_for_student"),
    path("students/<int:student_id>/<int:course_id>/add/", add_course_for_student, name="add_student_to_course"),
    path("professor-courses/add/", add_professor_course, name="add_professor_course"),
]
