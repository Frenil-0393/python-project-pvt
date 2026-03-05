from django.urls import path

from . import views

app_name = "organizer"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("schedule/", views.schedule_view, name="schedule"),
    path("scores/", views.scores_view, name="scores"),
    path("players/", views.players_view, name="players"),
]
