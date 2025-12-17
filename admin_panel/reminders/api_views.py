from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import json
from .models import Event
from .serializers import EventSerializer

# 1. Список усіх подій (JSON)
def api_event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return JsonResponse(serializer.data, safe=False)

# 2. Створення нової події (JSON або form-data)
@csrf_exempt
def create_event(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            return JsonResponse({"id": event.id}, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    elif request.content_type.startswith("multipart/form-data"):
        user_id = request.POST.get("user_id")
        text = request.POST.get("text", "")
        date = request.POST.get("date")
        time = request.POST.get("time")
        location = request.POST.get("location", "")
        link = request.POST.get("link", "")
        is_sent = request.POST.get("is_sent") == "true"
        added_to_calendar = request.POST.get("added_to_calendar") == "true"
        photo = request.FILES.get("photo")

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return JsonResponse({"user_id": ["A valid integer is required."]}, status=400)

        event = Event.objects.create(
            user_id=user_id,
            text=text,
            date=date,
            time=time,
            location=location,
            link=link,
            is_sent=is_sent,
            added_to_calendar=added_to_calendar,
            photo=photo,
        )

        return JsonResponse({
            "id": event.id,
            "photo": event.photo.url if event.photo else None
        }, status=201)

    else:
        return HttpResponseBadRequest("Unsupported content type")

# 3. Перегляд конкретної події за ID
def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    serializer = EventSerializer(event)
    return JsonResponse(serializer.data)

# 4. Оновлення події
@csrf_exempt
def update_event(request, event_id):
    if request.method != "PUT":
        return HttpResponseBadRequest("Only PUT allowed")

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    serializer = EventSerializer(event, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"status": "updated", "id": event.id})
    else:
        return JsonResponse(serializer.errors, status=400)

# 5. Видалення події
@csrf_exempt
def delete_event(request, event_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Only DELETE allowed")

    deleted, _ = Event.objects.filter(id=event_id).delete()
    if deleted == 0:
        return HttpResponseNotFound("Event not found")
    return JsonResponse({"status": "deleted", "id": event_id})
