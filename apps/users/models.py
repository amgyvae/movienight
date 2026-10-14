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


class Friendship(models.Model):
    """Connection friendship between users"""
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Waiting pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected")
    )

    from_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="sent_friendships", 
        verbose_name="Sender"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_friendships",
        verbose_name="Receiver"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Status"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Application date"
    )

    class Meta:
        verbose_name = "Friendship"
        verbose_name_plural = "Friendships and applications"
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"],
                name="unique_friendship_request"
            )
        ]
        ordering = ["-created_at"]

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("Not allowed to send an application for yourself")

    def __str__(self) -> str:
        return f"{self.from_user.username} -> {self.to_user.username} ({self.get_status_display()})"