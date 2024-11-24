from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import random
from django.contrib.auth import get_user_model
from books.models import Book 

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    reference_id = models.CharField(max_length=6, unique=True, editable=False)  # 6-digit random reference ID    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    onboarding_completed = models.BooleanField(default=False)  # New field for tracking onboarding completion


    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Unique related_name to avoid clashes
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_user_permissions",  # Unique related_name to avoid clashes
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})" if self.first_name and self.last_name else self.username

    def save(self, *args, **kwargs):
        # Generate a random 6-digit reference ID before saving if not already set
        if not self.reference_id:
            self.reference_id = str(random.randint(100000, 999999))  # Random 6-digit number
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        

class UserInterest(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True)  # Icon class name or URL

    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"


class Onboarding(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="onboarding")
    is_student = models.BooleanField(default=False)
    interests = models.ManyToManyField(UserInterest, related_name="users")
    goal = models.CharField(
        max_length=100,
        choices=[
            ('knowledge', 'To expand my knowledge and skills'),
            ('entertainment', 'For personal enjoyment and relaxation'),
            ('education', 'To enhance my academic understanding and performance'),
            ('career', 'To improve my career prospects and professional growth'),
            ('social_interaction', 'To engage with and learn from others'),
            ('personal_growth', 'For personal growth and self-development'),
        ],
        blank=True,
        null=True
    )
    completed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Onboarding for {self.user.username}"

    class Meta:
        verbose_name = "Onboarding"
        verbose_name_plural = "Onboardings"

