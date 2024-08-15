from django.contrib.auth.models import User
from django.db import models

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    reference_id = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
