from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


from apps.users.models import Friendship, User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "letterboxd_username",
        "is_active",
        "is_staff",
        "created_at",
        #after adding preferences: "get_ratings_count",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )
    search_fields = (
        "username",
        "email",
        "letterboxd_username",
    )
    ordering = ("-created_at",)
    list_per_page = 25
    readonly_fields = ("created_at", "last_login")
    actions = [
        "deactivate_selected_users",
        "activate_selected_users"
    ]
    #in the future inlines:

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "avatar", "letterboxd_username", "bio")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "data_joined", "created_at")}),
    )

    @admin.display(description="Rating")
    def get_rating_count(self, obj: User) -> int:
        return obj.ratings.count()

    @admin.action(description="Deactivate selected users")
    def deactivate_selected_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Succesfully deactivated {count} users!")

    @admin.action(description="Activate selected users")
    def activate_selected_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Succesfully activated {count} users!")


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("from_user__username", "to_user__username")
    ordering = ("-created_at",)
    list_per_page = 25
    autocomplete_fields = ("from_user", "to_user")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"