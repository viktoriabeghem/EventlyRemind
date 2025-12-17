from django.urls import path
from .api_views import api_event_list, create_event, event_detail, update_event, delete_event
from . import views

urlpatterns = [
    # API маршрути
    path("api/events/", api_event_list, name="api_event_list"),
    path("api/events/create/", create_event, name="create_event"),
    path("api/events/<int:event_id>/", event_detail, name="event_detail"),
    path("api/events/<int:event_id>/update/", update_event, name="update_event"),
    path("api/events/<int:event_id>/delete/", delete_event, name="delete_event"),

    # HTML-шаблон
    path("events/", views.event_list, name="event_list"),

    # Головна сторінка → перенаправлення на /events/
    path("", views.event_list),
]
