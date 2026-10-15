from django.conf import settings
from django.db.models import (
    CharField, 
    DateField, 
    ForeignKey, 
    FloatField, 
    IntegerField,
    PositiveBigIntegerField,
    FileField,
    TextField, 
    DateTimeField,
    Model,
    UniqueConstraint,
    PROTECT,
    SET_NULL,
)

from apps.movies.models import Genre, Person, Movie


MIN_RATING = 0.0
MAX_RATING = 10.0


class UserRating(Model):

    SOURCE_MAX_LEN = 20
    SOURCE_LETTERBOXD = "letterboxd"
    SOURCE_MANUAL = "manual"
    SOURCE_CHOICES = (
        (SOURCE_LETTERBOXD, "Letterboxd"),
        (SOURCE_MANUAL, "Manual"),
    )

    user = ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = PROTECT,
        related_name = 'ratings',
        verbose_name = 'User',
    )
    movie = ForeignKey(
        to = 'movies.Movie',
        on_delete = PROTECT,
        related_name = 'ratings',
        verbose_name = 'Movie',
    )
    raw_rating = FloatField(
        verbose_name = 'Raw rating',
    )
    normalized_rating = FloatField(
        verbose_name = 'Normalized rating',
    )
    source = CharField(
        max_length = SOURCE_MAX_LEN,
        choices = SOURCE_CHOICES,
        default = SOURCE_MANUAL,
        verbose_name = 'Source',
        )
    watched_at = DateField(
        null=True, 
        blank=True,
        verbose_name = 'Watched at'
        )
    review = TextField(
        null=True, 
        blank=True,
        verbose_name = 'Review'
        )

    class Meta:

        verbose_name = 'User rating'
        verbose_name_plural = 'User ratings'

        constraints = [
            UniqueConstraint(
            fields=("user", "movie"),
            name="unique_user_movie_rating",
            ),
        ]
        
    def __str__(self) -> str:
        return f"{self.user} - {self.movie}: {self.normalized_rating}"


class ImportJob(Model):

    STATUS_MAX_LEN = 20
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'falied'
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completted"),
        (STATUS_FAILED, "Failed")
    )

    user = ForeignKey(
        to = settings.AUTH_USER_MODEL, 
        on_delete = PROTECT, 
        related_name = 'import_jobs',
        verbose_name = 'User',
    )
    source = CharField(
        max_length = UserRating.SOURCE_MAX_LEN, 
        choices = UserRating.SOURCE_CHOICES,
        default = UserRating.SOURCE_LETTERBOXD,
        verbose_name = 'Source',
    )
    file = FileField(
        upload_to = "imports/",
        verbose_name = 'File',
    )
    status = CharField(
        max_length = STATUS_MAX_LEN, 
        choices = STATUS_CHOICES,
        default = STATUS_PENDING,
        verbose_name = 'Status', 
    )
    total = PositiveBigIntegerField(
        default = 0,
        verbose_name = 'Total rows', 
    )
    matched = PositiveBigIntegerField(
        default = 0,
        verbose_name = 'Matched rows'
    )
    failed = PositiveBigIntegerField(
        default = 0,
        verbose_name = 'Failed rows'
    )
    created_at = DateTimeField(
        auto_now_add = 'True',
        verbose_name = 'Created at'
    )

    class Meta: 

        verbose_name = 'Import job'
        verbose_name_plural = 'Import jobs'

    def str(self) -> str:
        return f"Imported #{self.pk} by {self.user} ({self.status})"


class UnmatchedEntry(Model):

    TITLE_MAX_LENGTH = 255

    job = ForeignKey(
        to = ImportJob, 
        on_delete = PROTECT,
        related_name = 'unmatched_entries',
        verbose_name = 'Import job'
    )
    title = CharField(
        max_length = TITLE_MAX_LENGTH,
        verbose_name = 'Title'
    )
    year = IntegerField(
        null = True, 
        blank = True,
        verbose_name = 'Year'
    )
    raw_rating = FloatField(
        null = True, 
        blank = True,
        verbose_name = 'Raw rating'
    )
    resolved_movie = ForeignKey(
        to = 'movies.Movie', 
        on_delete = SET_NULL, 
        null = True, 
        blank = True,
        related_name = 'unmatched_entries',
        verbose_name = 'Resolved Movie',
    )

    class Meta: 

        verbose_name = 'Unmatched Entry'
        verbose_name_plural = 'Unmatched Entries'

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"


class TasteProfile(Model):

    user = ForeignKey(
        to = settings.AUTH_USER_MODEL, 
        on_delete = PROTECT, 
        related_name = 'taste_profiles',
        verbose_name = 'User'
    )
    genre = ForeignKey(
        to = 'movies.Genre', 
        on_delete = PROTECT, 
        null = True, 
        blank = True,
        related_name = 'taste_genre',
        verbose_name = 'Genre'
    )
    person = ForeignKey(
        to = 'movies.Genre', 
        on_delete = PROTECT, 
        null = True, 
        blank = True,
        related_name = 'taste_person',
        verbose_name = 'Person'
    )
    weight = FloatField(
        default = 0.0,
        verbose_name = 'Weight',
    )
    updated_at = DateTimeField(
        auto_now_add = True, 
        verbose_name = 'Updated at'
    )

    class Meta:

        verbose_name = 'Taste Profile' 
        verbose_name_plural = 'Taste Profiles'

    def __str__(self) -> str:
        return f"{self.user} - {self.genre or self.person}: {self.weight}"


class WatchlistItem(Model):

    user = ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = PROTECT, 
        related_name = 'watchlist',
        verbose_name = 'User', 
    )
    movie = ForeignKey(
        to = 'movies.Movie',
        on_delete = PROTECT, 
        related_name = 'watchlist_item',
        verbose_name = 'Movie',
    )
    added_at = DateTimeField(
        auto_now_add = True, 
        verbose_name = 'Added at'
    )

    class Meta: 
        verbose_name = 'Watchlist item'
        verbose_name_plural = 'Watchlist items'

        constraints = [
            UniqueConstraint(
                fields = ("user", "movie"),
                name = "unique_user_movie_watchlist"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} wants to watch {self.movie}"
