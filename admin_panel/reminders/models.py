from django.db import models

class Event(models.Model):
    user_id = models.BigIntegerField()
    text = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    photo = models.ImageField(upload_to="event_photos/", blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    added_to_calendar = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({self.date} {self.time})"
