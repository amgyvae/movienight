from django.contrib import admin


from apps.voting.models import Vote, Result


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "candidate", "value")
    list_filter = ("value",)
    search_fields = ("user__username",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "movie", "likes_count")
    search_fields = ("movie__title",)