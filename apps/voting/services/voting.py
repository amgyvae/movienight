from django.db import transaction
from apps.voting.models import Candidate, Vote
from django.db.models import Count, Q
from django.utils import timezone
from apps.voting.models import Result, VotingSession
from apps.voting.services.recommender import (
    select_top_candidates,
    calculate_group_score
)


def get_next_candidate(session, user):

    candidate = session.candidates.exclude(
        votes__user=user
    ).order_by("position").first()

    return candidate


def cast_vote(session, candidate_id, user, value):

    if value not in ["like", "dislike"]:
        raise ValueError("Invalid vote")

    with transaction.atomic():

        session = VotingSession.objects.select_for_update().get(
            pk=session.pk
        )

        if session.status != "in_progress":
            raise ValueError("Voting is completed")

        member_ids = list(
            session.room.members.values_list(
                "user_id", flat=True
            )
        )

        if user.pk not in member_ids:
            raise ValueError("User is not a room member")

        candidate = Candidate.objects.get(
            id=candidate_id,
            session=session
        )

        vote, created = Vote.objects.get_or_create(
            candidate=candidate,
            user=user,
            defaults={"value": value}
        )

        if not created:
            raise ValueError("Already voted")

        total_members = len(member_ids)

        total_candidates = session.candidates.count()

        total_votes = Vote.objects.filter(
            candidate__session=session,
            user_id__in=member_ids
        ).count()

        expected_votes = total_members * total_candidates

        if total_candidates > 0 and total_votes == expected_votes:
            finalize_voting_session(session)

    return vote



    
def finalize_voting_session(session):

    with transaction.atomic():

        session = VotingSession.objects.select_for_update().get(
            pk=session.pk
        )

        if session.status == "completed":
            return Result.objects.filter(session=session).first()

        candidates = session.candidates.annotate(
            likes_count=Count(
                "votes",
                filter=Q(votes__value="like")
            )
        ).order_by(
            "-likes_count",
            "-group_score",
            "position"
        )

        winner = candidates.first()

        if winner is None:
            raise ValueError("No candidates found")

        result = None

        if winner.likes_count > 0:
            result, created = Result.objects.get_or_create(
                session=session,
                defaults={
                    "movie": winner.movie,
                    "likes_count": winner.likes_count
                }
            )

        session.status = "completed"
        session.finished_at = timezone.now()

        session.save(
            update_fields=["status", "finished_at"]
        )

        return result



def start_session(room, movies, watched_movie_ids=None):

    if watched_movie_ids is None:
        watched_movie_ids = set()

    selected_movies = select_top_candidates(
        movies,
        watched_movie_ids,
        limit=12
    )

    if not selected_movies:
        raise ValueError("No movies available")

    with transaction.atomic():

        if VotingSession.objects.filter(
            room=room,
            status="in_progress"
        ).exists():
            raise ValueError("Voting already started")

        last_session = VotingSession.objects.filter(
            room=room
        ).order_by("-round_number").first()

        round_number = 1

        if last_session:
            round_number = last_session.round_number + 1

        if round_number > 3:
            raise ValueError("Maximum rounds reached")

        session = VotingSession.objects.create(
            room=room,
            round_number=round_number,
            status="in_progress"
        )

        for position, movie in enumerate(selected_movies, start=1):

            Candidate.objects.create(
                session=session,
                movie_id=movie["id"],
                group_score=calculate_group_score(
                    movie["scores"]
                ),
                position=position
            )

        room.status = "voting"
        room.save(update_fields=["status"])

    return session

def start_next_round(session, movies, watched_movie_ids=None):

    if session.status != "completed":
        raise ValueError("Current round is not completed")

    if session.round_number >= 3:
        return None

    if Result.objects.filter(session=session).exists():
        return None

    previous_movies = set(
        Candidate.objects.filter(
            session__room=session.room
        ).values_list("movie_id", flat=True)
    )

    excluded_movies = previous_movies | set(
        watched_movie_ids or []
    )

    return start_session(
        room=session.room,
        movies=movies,
        watched_movie_ids=excluded_movies
    )