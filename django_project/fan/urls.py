from django.urls import path

from . import views

app_name = "fan"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("timetable/", views.timetable_view, name="timetable"),
    path("live-scores/", views.live_scores_view, name="live_scores"),
    path("stats/", views.stats_view, name="stats"),
    path("leaderboard/", views.leaderboard_view, name="leaderboard"),
    path("highlights/", views.highlights_view, name="highlights"),
]
