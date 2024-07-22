# models.py
from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_event_id = models.CharField(max_length=255, unique=True)
    summary = models.CharField(max_length=255)
    start = models.DateTimeField()
    
    def __str__(self):
        return f"{self.summary} - {self.start}"
