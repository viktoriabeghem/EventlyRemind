from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import json
from .models import Event

# 1. Список усіх подій
def event_list(request):
    events = Event.objects.all()
    data = []
    for event in events:
        data.append({
            "id": event.id,
            "user_id": event.user_id,
            "text": event.text,
            "date": event.date.strftime("%Y-%m-%d") if event.date else None,
            "time": event.time.strftime("%H:%M") if event.time else None,
            "location": event.location,
            "link": event.link,
            "photo": event.photo.url if event.photo else None,
            "is_sent": event.is_sent,
            "added_to_calendar": event.added_to_calendar,
        })
    return JsonResponse(data, safe=False)

# 2. Створення нової події
@csrf_exempt
def create_event(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    event = Event.objects.create(
        user_id=data.get("user_id"),
        text=data.get("text", ""),
        date=data.get("date"),
        time=data.get("time"),
        location=data.get("location", ""),
        link=data.get("link", ""),
        is_sent=data.get("is_sent", False),
        added_to_calendar=data.get("added_to_calendar", False),
    )

    return JsonResponse({"id": event.id}, status=201)

# 3. Перегляд конкретної події за ID
def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    data = {
        "id": event.id,
        "user_id": event.user_id,
        "text": event.text,
        "date": event.date.strftime("%Y-%m-%d") if event.date else None,
        "time": event.time.strftime("%H:%M") if event.time else None,
        "location": event.location,
        "link": event.link,
        "photo": event.photo.url if event.photo else None,
        "is_sent": event.is_sent,
        "added_to_calendar": event.added_to_calendar,
    }
    return JsonResponse(data)
