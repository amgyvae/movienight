from django.contrib import admin 

from apps.preferences.models import (
    ImportJob,
    TasteProfile, 
    UnmatchedEntry, 
    UserRating, 
    WatchlistItem,
)

@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = (
        "user", 
        "movie",
        "raw_rating", 
        "normalized_rating", 
        "source", 
        "watched_at",
        "review", 
    )
    list_filter = ('source', )
    search_fields = ('user__username', 'movie__title')

@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "user", 
        "source", 
        "file", 
        "status", 
        "total", 
        "matched", 
        "failed", 
        "created_at", 
    )
    list_filter = ("status", "source",)
    search_fields = ("user__username",)
    readonly_fields = ("total", "matched", "failed", "created_at",)

@admin.register(UnmatchedEntry)
class UnmatchedEntryAdmin(admin.ModelAdmin):
    list_display = (
        "title", 
        "year", 
        "raw_rating", 
        "job", 
        "resolved_movie", 
    )
    search_fileds = ("title",)

@admin.register(TasteProfile)
class TasteProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user", 
        "genre", 
        "person",
        "weight", 
        "updated_at",
        )
    list_filter = ("genre",)
    search_fileds = ("user__username",)
    readonly_fields = ("updated_at",)

@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = (
        "user", 
        "movie", 
        "added_at"
    )
    search_fileds = ("user__username", "movie__title",)
    readonly_fields = ("added_at",)