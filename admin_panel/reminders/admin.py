from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("text", "date", "time", "location", "is_sent", "added_to_calendar")
    list_filter = ("date", "is_sent", "added_to_calendar")
    search_fields = ("text", "location")
