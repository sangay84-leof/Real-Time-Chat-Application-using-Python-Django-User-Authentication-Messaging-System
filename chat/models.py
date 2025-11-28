from django.db import models

class Message(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar_color = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.timestamp.strftime('%H:%M')} - {self.text}"
