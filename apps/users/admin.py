from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import Friendship, User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
        "letterboxd_username",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username", "letterboxd_username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "last_login")
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Profile", {"fields": ("avatar", "letterboxd_username", "bio")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups")},
        ),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("from_user__username", "to_user__username")
    readonly_fields = ("created_at", "updated_at")
