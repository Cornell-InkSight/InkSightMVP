from django.urls import path
from .api import *

urlpatterns = [
   path('image-preprocessing', preprocess_image, name="preprocess_image"),
   path('send-to-kafka', send_video_data_to_kafka, name="send_video_data_to_kafka")
]
