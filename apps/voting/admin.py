from django.contrib import admin
from django.db.models import Count


from apps.voting.models import Vote, Result


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "candidate", "colored_value", "voted_at")
    list_filter = ("value", "voted_at")
    search_fields = ("user__username", "candidate__movie__title")
    autocomplete_fields = ("user", "candidate")
    ordering = ("-voted_at",)
    date_hierarchy = "voted_at"

    @admin.display(description="Голос")
    def colored_value(self, obj: Vote) -> str:
        if obj.value == Vote.VALUE_LIKE:
            return format_html('<span style="color: green; font-weight: bold;">❤️ Like</span>')
        return format_html('<span style="color: red; font-weight: bold;">✖️ Dislike</span>')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("session", "movie", "likes_count")
    autocomplete_fields = ("session", "movie")
    search_fields = ("movie__title", "session__room__name")