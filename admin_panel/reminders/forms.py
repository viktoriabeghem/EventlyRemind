from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['text', 'date', 'time', 'location', 'link', 'photo', 'is_sent', 'added_to_calendar']
