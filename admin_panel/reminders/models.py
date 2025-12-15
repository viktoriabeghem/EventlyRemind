from django.db import models

class Event(models.Model):
    # Якщо ти не використовуєш Django User, можна залишити user_id
    user_id = models.BigIntegerField(null=True, blank=True)

    text = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    photo = models.ImageField(upload_to="event_photos/", blank=True, null=True)

    is_sent = models.BooleanField(default=False)
    added_to_calendar = models.BooleanField(default=False)

    def __str__(self):
        # Показує текст події та дату/час, якщо вони є
        date_str = self.date.strftime("%Y-%m-%d") if self.date else "no date"
        time_str = self.time.strftime("%H:%M") if self.time else "no time"
        return f"{self.text} ({date_str} {time_str})"
