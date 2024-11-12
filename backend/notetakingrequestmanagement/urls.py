from django.urls import path
from .api import *

urlpatterns = [
    path("notetaking-request/", get_note_taking_requests, name="get_notes_packets"),
    path("notetaking-request/<int:note_taking_request_id>/", get_note_taking_request, name="get_note_packet"),
    path("notetaking-request/add/", add_note_taking_request, name="add_note_taking_request"),
    path("courses/<int:course_id>/note-packets", get_note_taking_request_request_for_course, name="get_note_taking_request_request_for_course"),
    path("courses/<int:course_id>/approved-students", get_approved_students_for_notetaking_packets_for_course, 
    name="get_approved_students_for_notetaking_packets_for_course"),
    path("notetaking-request/<int:notetaking_request_id>/approve", approve_notetaking_request, name="approve_notetaking_request"),
    path("notetaking-request/<int:student_id>/<int:course_id>/", get_student_notetaking_request_for_course, name="get_student_notetaking_request_for_course"),
    path("notetaking-request/<int:student_id>/<int:course_id>/approved", get_is_student_approved_for_course, name="get_is_student_approved_for_course")

]
