from django.urls import path
from .api import *

urlpatterns = [
    path("lecture-sessions/", get_lecture_sessions, name="get_lecture_sessions"),
    path("lecture-sessions/<int:lecture_session_id>/", get_lecture_session, name="get_lecture_session"),
    path("recording-sessions/", get_recording_sessions, name="get_recording_sessions"),
    path("recording-sessions/<int:recording_session_id>/", get_recording_session, name="get_recording_session"),
    path("lecture-sessions/add/", add_lecture_session, name="add_lecture_session"),
    path("lecture-sessions/<int:lecture_session_id>/update", update_lecture_session_status, name="update_lecture_session_status"),
    path("recording-sessions/add/", add_recording_session, name="add_recording_session"),
    path("<int:course_id>/current-lecture-session", get_current_lecture_session_for_course, name="get_current_lecture_session_for_course"),
    path("lecture-sessions/<int:course_id>/upload_slides", upload_lecture_session_slides, name="upload_lecture_session_slides"),
    path("lecture-sessions/<int:lecture_session_id>/<int:slides_id>", set_lecture_session_for_slides, name="set_lecture_session_for_slides")
]
