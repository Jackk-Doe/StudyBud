from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)       #Get current time every saved
    created = models.DateTimeField(auto_now_add=True)   #Get first time created

    class Meta:
        ordering = ['-updated', '-created'] #Ordering Newest first
        # ordering = ['updated', 'created'] #Ordering Oldest first

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] #Ordering Newest first

    def __str__(self):
        return self.body[:50]