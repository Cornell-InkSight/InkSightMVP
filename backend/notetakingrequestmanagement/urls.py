from django.urls import path
from .api import *

urlpatterns = [
    path("notes-packets/", get_notes_packets, name="get_notes_packets"),
    path("notes-packets/<int:note_packet_id>/", get_note_packet, name="get_note_packet"),
    path("notes-packets/add/", add_note_taking_request, name="add_note_taking_request"),
]
