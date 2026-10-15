from django.contrib import admin

from apps.movies.models import Genre, Movie, MovieCredit, Person


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

class MovieCreditInline(admin.TabularInline):
    """"""


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """"""


@admin.register(MovieCredit)
class MovieCreditAdmin(admin.ModelAdmin):
    pass
