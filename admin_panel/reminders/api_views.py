from django.http import JsonResponse
from .models import Event

def event_list(request):
    events = Event.objects.all()
    data = [
        {
            "id": event.id,
            "user_id": event.user_id,
            "text": event.text,
            "date": event.date.strftime("%Y-%m-%d"),
            "time": event.time.strftime("%H:%M"),
            "location": event.location,
            "link": event.link,
            "photo": event.photo.url if event.photo else None,
            "is_sent": event.is_sent,
            "added_to_calendar": event.added_to_calendar,
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)
