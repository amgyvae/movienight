from django.contrib import admin
from django.urls import path
from django.urls import path, include
from apps.voting import views as voting_views

voting_patterns = [
    path(
        "<int:session_id>/",
        voting_views.swipe_view,
        name="swipe"
    ),
    path(
        "<int:session_id>/vote/",
        voting_views.vote_view,
        name="vote"
    ),
    path(
        "<int:session_id>/result/",
        voting_views.result_view,
        name="result"
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "voting/",
        include((voting_patterns, "voting"), namespace="voting")
    ),
]