from django.db import models
from users.models import Profile

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    manager = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="branch_manager")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name