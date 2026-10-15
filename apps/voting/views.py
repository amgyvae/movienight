from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.voting.models import VotingSession, Candidate, Result
from apps.voting.services.voting import (
    get_next_candidate,
    cast_vote,
)


def get_user_session(session_id, user):
    session = get_object_or_404(
        VotingSession,
        pk=session_id
    )

    if not session.room.members.filter(user=user).exists():
        raise PermissionDenied

    return session


@login_required
def swipe_view(request, session_id):
    session = get_user_session(session_id, request.user)

    if session.status == "completed":
        return redirect("voting:result", session_id=session.id)

    candidate = get_next_candidate(session, request.user)

    return render(request, "voting/swipe.html", {
        "session": session,
        "candidate": candidate,
    })


@login_required
@require_POST
def vote_view(request, session_id):
    session = get_user_session(session_id, request.user)

    candidate_id = request.POST.get("candidate_id")
    value = request.POST.get("value")

    try:
        cast_vote(session, candidate_id, request.user, value)
    except (ValueError, ValidationError, Candidate.DoesNotExist) as error:
        return JsonResponse({"error": str(error)}, status=400)

    session.refresh_from_db()

    if session.status == "completed":
        result_exists = Result.objects.filter(session=session).exists()

        return JsonResponse({
            "status": "completed",
            "result_url": reverse(
                "voting:result",
                args=[session.id]
            ),
            "has_winner": result_exists,
        })

    candidate = get_next_candidate(session, request.user)

    if candidate is None:
        return JsonResponse({"status": "waiting"})

    return JsonResponse({
        "status": "next",
        "candidate_id": candidate.id,
        "movie_title": str(candidate.movie),
        "group_score": candidate.group_score,
    })


@login_required
def result_view(request, session_id):
    session = get_user_session(session_id, request.user)

    if session.status != "completed":
        return redirect("voting:swipe", session_id=session.id)

    result = Result.objects.filter(
        session=session
    ).select_related("movie").first()

    return render(request, "voting/result.html", {
        "session": session,
        "result": result,
    })  