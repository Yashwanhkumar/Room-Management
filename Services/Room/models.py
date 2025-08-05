from django.db import models
from django.contrib.auth.models import User
import uuid

def generate_invite_code():
    """Generates a unique 8-character invite code."""
    return uuid.uuid4().hex[:8].upper()

class Room(models.Model):
    """Represents a room that users can join."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    invite_code = models.CharField(max_length=8, default=generate_invite_code, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rooms')
    members = models.ManyToManyField(User, related_name='rooms', blank=True)

    def __str__(self):
        return self.name

class Allservices(models.Model):
    """Represents a service that belongs to a specific room."""
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='services')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.service_name

class ServiceRecord(models.Model):
    """Stores individual records for a service, including cost."""
    service = models.ForeignKey(Allservices, on_delete=models.CASCADE, related_name='records')
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.service.service_name}"