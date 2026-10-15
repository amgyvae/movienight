from django.contrib import admin
from django.utils.html import format_html

from apps.movies.models import Genre, Movie, MovieCredit, Person


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "tmdb_id")
    search_fields = ("name",)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "known_for", "tmdb_id")
    list_filter = ("known_for",)
    search_fields = ("name",)

class MovieCreditInline(admin.TabularInline):
    model = MovieCredit
    extra = 1

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "poster_preview",
        "tmdb_rating",
        "popularity",
    )
    list_filter = ("year", "genres")
    search_fields = ("title", "original_title")
    inlines = [MovieCreditInline]
    filter_horizontal = ("genres",)

    @admin.display(description="Постер")
    def poster_preview(self, obj):
        if not obj.full_poster_url:
            return "Нет постера"
        return format_html(
            '<img src="{}" height="60"/>',
            obj.full_poster_url,
        )

@admin.register(MovieCredit)
class MovieCreditAdmin(admin.ModelAdmin):
    list_display = ("movie", "person", "role")
    list_filter = ("role",)
