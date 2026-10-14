from django.conf import settings
from django.db import models


MIN_RATING = 0.0
MAX_RATING = 10.0


class UserRating(models.Model):

    SOURCE_MAX_LEN = 20

    class Source(models.TextChoices):

        LETTERBOXD = 'letterboxd', 'Letterboxd'
        MANUAL = 'manual', 'Вручную'

        user = models.Foriegnkey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE,
            related_name = 'ratings',
        )
        movie = models.Foriegnkey(
            'movies.Movie'
            on_delete = models.CASCADE,
        )
        raw_rating = models.FloatField()
        normalized_rating = models.FloatField()
        source = models.CharField(
            max_length = SOURCE_MAX_LEN,
            choices = Source.choices,
            default = Source.MANUAL,

        )
        watched_at = models.DateField(null=True, blank=True)
        # review = models.TextField(null=True, blank=True)

        class Meta:
            verbose_name = 'User rating'
            verbose_name_plural = 'User ratings'

class ImportJob()