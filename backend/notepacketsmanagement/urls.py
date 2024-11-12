from django.urls import path
from .api import *

urlpatterns = [
    path('notes-packets/', get_notes_packets, name="get_notes_packets"),
    path('notes-packets/<int:note_packet_id>/', get_note_packet, name="get_note_packet"),
    path('notes-packets/add/', add_notes_packet, name="add_notes_packet"),
    path('courses/<int:course_id>/notes-packets', get_note_packets_for_course, name="get_note_packets_for_course"),
    path('courses/<int:course_id>/notes-packets-published', get_published_note_packets_for_course, name="get_published_note_packets_for_course"),
    path('courses/<int:course_id>/notes-packets-unpublished', get_unpublished_note_packets_for_course, name="get_unpublished_note_packets_for_course"),
    path('notes-packet/<int:note_packet_id>/update', update_notes_packet_status, name="update_notes_packet_status"),
]
