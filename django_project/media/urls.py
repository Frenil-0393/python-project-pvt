from django.urls import path

from . import views

app_name = "media"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("broadcast/", views.broadcast_view, name="broadcast"),
    path("highlights/", views.highlights_view, name="highlights"),
    path("press/", views.press_view, name="press"),
    path("press/export/", views.export_press_csv, name="export_press"),
]
