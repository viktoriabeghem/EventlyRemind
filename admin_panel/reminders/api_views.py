from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from .models import Event
from .forms import EventForm
from .serializers import EventSerializer
import json

# 1. Список усіх подій
@require_http_methods(["GET"])
def api_event_list(request):
    events = Event.objects.all().order_by('-date', '-time')
    serializer = EventSerializer(events, many=True)
    return JsonResponse(serializer.data, safe=False)

# 2. Створення події (JSON або form-data)
@csrf_exempt
@require_http_methods(["POST"])
def create_event(request):
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        form = EventForm(data)
    else:
        form = EventForm(request.POST, request.FILES)

    if form.is_valid():
        event = form.save()
        return JsonResponse({
            "id": event.id,
            "text": event.text,
            "date": str(event.date),
            "time": str(event.time),
            "location": event.location,
            "link": event.link,
            "is_sent": event.is_sent,
            "added_to_calendar": event.added_to_calendar,
            "photo": event.photo.url if event.photo else None
        }, status=201)
    else:
        return JsonResponse(form.errors, status=400)

# 3. Деталі події
@require_http_methods(["GET"])
def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    serializer = EventSerializer(event)
    return JsonResponse(serializer.data)

# 4. Оновлення події (PATCH)
@csrf_exempt
@require_http_methods(["PATCH"])
def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    form = EventForm(data, instance=event, partial=True)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "updated", "id": event.id})
    else:
        return JsonResponse(form.errors, status=400)

# 5. Видалення події
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        return JsonResponse({"status": "deleted", "id": event_id})
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")
