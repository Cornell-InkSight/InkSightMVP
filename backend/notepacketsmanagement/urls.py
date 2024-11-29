from django.urls import path
from .api import *

urlpatterns = [
    path('notes-packets/', get_notes_packets, name="get_notes_packets"),
    path('notes-packets/<int:note_packet_id>/', get_note_packet, name="get_note_packet"),
    path('notes-packets/add/', add_notes_packet, name="add_notes_packet"),
    path('courses/<int:course_id>/notes-packets', get_note_packets_for_course, name="get_note_packets_for_course"),
    path('courses/<int:course_id>/notes-packets-published', get_published_note_packets_for_course, name="get_published_note_packets_for_course"),
    path('courses/<int:course_id>/notes-packets-unpublished', get_unpublished_note_packets_for_course, name="get_unpublished_note_packets_for_course"),
    
    path('student-notes-packets/', get_student_notes_packets, name="get_student_notes_packets"),
    path('student-notes-packets/<int:student_note_packet_id>/', get_student_note_packet, name="get_student_note_packet"),
    path('student-notes-packets/add/', add_student_note_packet, name="add_student_notes_packet"),
    path('students/<int:student_id>/<int:course_id>/student-note-packets', get_student_note_packets_for_student_course, name="get_student_note_packets_for_student"),

    path('notes-packet/<int:note_packet_id>/update', update_notes_packet_status, name="update_notes_packet_status"),
    path('notes-packet/<int:note_packet_id>/edit', update_notes_packet_text, name="update_notes_packet_text"),
]
