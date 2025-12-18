from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event

def event_list(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')  # або повернути JSON, якщо це API
    else:
        form = EventForm()

    events = Event.objects.all().order_by('-date', '-time')
    return render(request, 'events/event_list.html', {'form': form, 'events': events})
