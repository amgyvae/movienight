import random
import string 

from django.conf import settings
from django.db import models

def generate_room_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=6))
class Room(models.Model):
    STATUS_CHOICES = [
        ("open", "Сбор"),
        ("voting", "Голосование"),
        ("finished", "Завершено"),
    ]
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_rooms",
    )
    
    code = models.CharField(
        max_length=12,
        unique=True,
        default=generate_room_code,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}({self.code})"

class RoomMember(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_ready = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "user"],
                name = "unique_room_member_pair",
            )
        ]
    def __str__(self) -> str:
        return f"{self.user} in {self.room}"