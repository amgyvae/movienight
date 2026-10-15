from typing import Any


from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    EmailField,
    ForeignKey,
    ImageField,
    TextField,
    UniqueConstraint,
)


from apps.core.models import AbstractBaseModel


class UserManager(BaseUserManager):
    """Custom User Manager to create users and superusers."""

    def create_user(
        self,
        email: str,
        username: str,
        password: str,
        **kwargs: Any,
    ) -> "User":
        """Create a regular user."""
        if not email:
            raise ValidationError(
                message="Email field is required.", code="email_empty"
            )
        if not username:
            raise ValidationError(
                message="Username field is required.", code="username_empty"
            )

        new_user: "User" = self.model(
            email=self.normalize_email(email).lower(),
            username=username,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        email: str,
        username: str,
        password: str,
        **kwargs: Any,
    ) -> "User":
        """Create a superuser. Used by manage.py createsuperuser."""
        return self.create_user(
            email=email,
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """Custom user model for the Movie Night app."""

    EMAIL_MAX_LENGTH = 254
    USERNAME_MAX_LENGTH = 150
    LETTERBOXD_USERNAME_MAX_LENGTH = 150

    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Email address",
    )
    username = CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name="Username",
    )
    avatar = ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name="Avatar",
    )
    letterboxd_username = CharField(
        max_length=LETTERBOXD_USERNAME_MAX_LENGTH,
        blank=True,
        default="",
        verbose_name="Letterboxd username",
    )
    bio = TextField(
        blank=True,
        default="",
        verbose_name="Bio",
    )
    # True if the user can open the admin panel
    is_staff = BooleanField(
        default=False,
        verbose_name="Staff status",
    )
    # True if the user can log in
    is_active = BooleanField(
        default=True,
        verbose_name="Active",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    class Meta:
        """Meta data for the table."""

        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.username

    @property
    def has_ratings(self) -> bool:
        """Check if the user has any movie ratings."""
        return self.ratings.exists()


class Friendship(AbstractBaseModel):
    """Friendship requests between users."""

    STATUS_MAX_LENGTH = 20
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
    )

    from_user = ForeignKey(
        to=User,
        on_delete=PROTECT,
        related_name="sent_friendships",
        verbose_name="Sender",
    )
    to_user = ForeignKey(
        to=User,
        on_delete=PROTECT,
        related_name="received_friendships",
        verbose_name="Receiver",
    )
    status = CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Status",
    )
    class Meta:
        """Meta data for the table."""

        verbose_name = "Friendship"
        verbose_name_plural = "Friendships"
        constraints = [
            UniqueConstraint(
                fields=("from_user", "to_user"),
                name="unique_friendship_request",
            )
        ]

    def clean(self) -> None:
        """Do not allow sending a friend request to yourself."""
        if self.from_user == self.to_user:
            raise ValidationError(
                message="You cannot send a friend request to yourself.",
                code="self_friendship",
            )

    def __str__(self) -> str:
        return (
            f"{self.from_user.username} -> {self.to_user.username} "
            f"({self.get_status_display()})"
        )
