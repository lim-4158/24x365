# models.py
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Event(models.Model):
    summary = models.CharField(max_length=255)
    start = models.DateTimeField()
    
    def __str__(self):
        return f"{self.summary} - {self.start}"