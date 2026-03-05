from django.contrib import messages
from django.shortcuts import redirect, render

from common.decorators import role_required
from media.models import BroadcastSession, Highlight, PressRelease
from organizer.models import Match


@role_required("media")
def dashboard(request):
	return render(request, "media/dashboard.html", {"user_name": request.user.first_name or "Media"})


@role_required("media")
def broadcast_view(request):
	if request.method == "POST":
		match_id = request.POST.get("match_id")
		channel_name = request.POST.get("channel_name", "").strip()
		stream_url = request.POST.get("stream_url", "").strip()
		is_live = request.POST.get("is_live") == "on"

		match = Match.objects.filter(id=match_id).first()
		if not match or not channel_name:
			messages.error(request, "Please select match and enter channel.")
			return redirect("media:broadcast")

		BroadcastSession.objects.create(
			match=match,
			channel_name=channel_name,
			stream_url=stream_url,
			is_live=is_live,
		)
		messages.success(request, "Broadcast session saved.")
		return redirect("media:broadcast")

	matches = Match.objects.all()
	broadcasts = BroadcastSession.objects.select_related("match").all()
	return render(request, "media/broadcast.html", {"matches": matches, "broadcasts": broadcasts})


@role_required("media")
def highlights_view(request):
	if request.method == "POST":
		match_id = request.POST.get("match_id")
		title = request.POST.get("title", "").strip()
		description = request.POST.get("description", "").strip()
		duration = request.POST.get("duration", "").strip()

		match = Match.objects.filter(id=match_id).first()
		if not match or not title:
			messages.error(request, "Please select match and enter highlight title.")
			return redirect("media:highlights")

		Highlight.objects.create(
			match=match,
			title=title,
			description=description,
			duration=duration,
		)
		messages.success(request, "Highlight published.")
		return redirect("media:highlights")

	matches = Match.objects.all()
	highlights = Highlight.objects.select_related("match").all()
	return render(request, "media/highlights.html", {"matches": matches, "highlights": highlights})


@role_required("media")
def press_view(request):
	if request.method == "POST":
		sport = request.POST.get("sport", "").strip()
		headline = request.POST.get("headline", "").strip()
		body = request.POST.get("body", "").strip()
		status = request.POST.get("status", PressRelease.STATUS_DRAFT)

		if not sport or not headline or not body:
			messages.error(request, "Please fill all press release fields.")
			return redirect("media:press")

		PressRelease.objects.create(sport=sport, headline=headline, body=body, status=status)
		messages.success(request, "Press release saved.")
		return redirect("media:press")

	press_releases = PressRelease.objects.all()
	return render(request, "media/press.html", {"press_releases": press_releases})
