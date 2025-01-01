from django.urls import path
from .consumers import LivestreamConsumer

websocket_urlpatterns = [
    path("ws/livestream/", LivestreamConsumer.as_asgi()),
]
