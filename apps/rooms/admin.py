from django.contrib import admin
from django.db.models import Count

from apps.rooms.models import Room, RoomMember


class RoomMemberInline(admin.TabularInline):
    model = RoomMember
    extra = 0
    fields = ("user", "is_ready", "joined_at")
    readonly_fields=("joined_at",)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "status", "owner", "members_count", "created_at")
    list_filter =("status", "created_at")
    search_fields = ("name", "code", "owner__username")
    readonly_fields=("code", "created_at")
    fieldsets=(
        ("Комната", {"fields": ("name", "owner","status")}),
        ("Служебное", {"fields":("code", "created_at")}),
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 20
    inlines=[RoomMemberInline]
    actions = ["close_rooms"]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("owner").annotate(
            members_total=Count("members")
        )
    @admin.display(description="Участников", ordering="members_total")
    def members_count(self, obj:Room) -> int:
        return obj.members_total

    @admin.action(description="Закрыть выбранные комнаты")
    def close_rooms(self, request, queryset):
        updated = queryset.order_by().update(status="finished")
        self.message_user(request, f"Закрыто комнат: {updated}")

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "is_ready", "joined_at")
    list_filter = ("is_ready", "room__status")
    search_fields = ("user__username", "room__name", "room__code")
    list_select_related=("user", "room")
    ordering = ("-joined_at",)
