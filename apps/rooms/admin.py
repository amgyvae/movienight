from django.contrib import admin
from apps.rooms.models import Room, RoomMember


class RoomMemberInline(admin.TabularInline):
    model = RoomMember
    extra = 0
    fields = ("user", "is_ready", "joined_at")
    readonly_fields=("joined_at",)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines=[RoomMemberInline]

admin.site.register(RoomMember)