from django.urls import path
from . import api_views

urlpatterns = [
    path("api/events/", api_views.event_list, name="event_list"),
]
