from django.urls import path
from .api import *

urlpatterns = [
   path('image-preprocessing', preprocess_image, name="preprocess_image")
]
