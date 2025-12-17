from django.shortcuts import render

def event_list(request):
    return render(request, "events/event_list.html")
