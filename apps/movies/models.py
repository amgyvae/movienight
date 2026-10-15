from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

ROLE_CHOICES = [
    ("actor", "Актер"),
    ("director", "Режиссер"),
]

class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Person(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    known_for = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
    )

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    year = models.PositiveBigIntegerField()
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    tmdb_rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0),
        ],
    )
    popularity = models.FloatField(default=0.0)

    genres = models.ManyToManyField(
        Genre,
        related_name="movies",
    )
    people = models.ManyToManyField(
        Person,
        through="MovieCredit",
    )

    def __str__(self):
        return f"{self.title} ({self.year})"

class MovieCredit(models.Model):
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )

    def __str__(self):
        return (
            f"{self.movie} - {self.person} "
            f"({self.get_role_display()})"
        )