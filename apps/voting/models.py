from django.db import models
from django.conf import settings


class VotingSession(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="voting_sessions"
    )

    round_number = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress"
    )

    started_at = models.DateTimeField(auto_now_add=True)

    finished_at = models.DateTimeField(null=True, blank=True)

class Candidate(models.Model):
    session = models.ForeignKey(
        VotingSession,
        on_delete=models.CASCADE,
        related_name="candidates"
    )

    movie = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE
    )

    group_score = models.FloatField()

    positon = models.PositiveIntegerField()


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "movie"],
                name="unique_session_candidate_movie"
            )
        ]


class Vote(models.Model):
    VOTE_CHOICES = [
        ("like", "Like"),
        ("dislike", "Dislike"),
    ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    value = models.CharField(max_length=10, choices=VOTE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "user"],
                name="unique_candidate_user_vote"
            )
        ]


class Result(models.Model):
    session = models.OneToOneField(
        VotingSession,
        on_delete=models.CASCADE,
        related_name="result"
    )

    movie = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE
    )

    likes_count = models.PositiveIntegerField()