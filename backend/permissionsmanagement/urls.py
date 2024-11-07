from django.urls import path
from .api import *

urlpatterns = [
    path("permissions/", get_permissions, name="get_permissions"),
    path("permissions/<int:note_packet_id>/", get_note_packet, name="get_note_packet"),
    path("permissions/add/", add_permissions, name="add_permissions"),
    path("permissions/assign_all/", assign_all_permissions, name="assign_all_permissions"),
]
