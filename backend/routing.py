from django.urls import path
from backend.quickstart import consumers

websocket_urlpatterns = [
    path("ws/hints/", consumers.HintConsumer.as_asgi())
]
