from django.urls import path
from .api_views import event_list, create_event, event_detail

urlpatterns = [
    path("api/events/", event_list, name="event_list"),
    path("api/events/create/", create_event, name="create_event"),
    path("api/events/<int:event_id>/", event_detail, name="event_detail"),
]