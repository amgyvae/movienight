from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """Custom User for Movie Night App"""
    email = models.EmailField(unique=True, verbose_name="Email Address")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Avatar")
    letterboxd_username = models.CharField(max_length=150, blank=True, default="", verbose_name="Letterboxd Username")
    bio = models.TextField(blank=True, default="", verbose_name="Bio")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def has_ratings(self) -> bool:
        """Check, user has ratings or not"""
        return self.ratings.exists()
    