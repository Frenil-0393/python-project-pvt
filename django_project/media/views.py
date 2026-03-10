from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
import csv

from common.decorators import role_required
from media.models import BroadcastSession, Highlight, PressRelease
from organizer.models import Match


@role_required("media")
def dashboard(request):
	return render(request, "media/dashboard.html", {"user_name": request.user.first_name or "Media"})


@role_required("media")
def broadcast_view(request):
	if request.method == "POST":
		action = request.POST.get("action", "create")
		if action == "toggle":
			broadcast_id = request.POST.get("broadcast_id")
			item = BroadcastSession.objects.filter(id=broadcast_id).first()
			if not item:
				messages.error(request, "Broadcast not found.")
			else:
				item.is_live = not item.is_live
				item.save(update_fields=["is_live", "updated_at"])
				messages.success(request, "Broadcast live status updated.")
			return redirect("media:broadcast")

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

	sort = request.GET.get("sort", "-updated_at").strip() or "-updated_at"
	matches = Match.objects.all()
	broadcasts = BroadcastSession.objects.select_related("match").order_by(sort)
	return render(request, "media/broadcast.html", {"matches": matches, "broadcasts": broadcasts, "sort": sort})


@role_required("media")
def highlights_view(request):
	if request.method == "POST":
		action = request.POST.get("action", "create")
		if action == "delete":
			highlight_id = request.POST.get("highlight_id")
			deleted, _ = Highlight.objects.filter(id=highlight_id).delete()
			if deleted:
				messages.success(request, "Highlight deleted.")
			else:
				messages.error(request, "Highlight not found.")
			return redirect("media:highlights")

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

	q = request.GET.get("q", "").strip()
	sort = request.GET.get("sort", "-published_at").strip() or "-published_at"
	matches = Match.objects.all()
	highlights = Highlight.objects.select_related("match").all()
	if q:
		highlights = highlights.filter(title__icontains=q)
	highlights = highlights.order_by(sort)
	return render(
		request,
		"media/highlights.html",
		{"matches": matches, "highlights": highlights, "q": q, "sort": sort},
	)


@role_required("media")
def press_view(request):
	if request.method == "POST":
		action = request.POST.get("action", "create")
		if action == "delete":
			press_id = request.POST.get("press_id")
			deleted, _ = PressRelease.objects.filter(id=press_id).delete()
			if deleted:
				messages.success(request, "Press release deleted.")
			else:
				messages.error(request, "Press release not found.")
			return redirect("media:press")
		if action == "set_status":
			press_id = request.POST.get("press_id")
			status = request.POST.get("status", PressRelease.STATUS_DRAFT)
			updated = PressRelease.objects.filter(id=press_id).update(status=status)
			if updated:
				messages.success(request, "Press status updated.")
			else:
				messages.error(request, "Press release not found.")
			return redirect("media:press")

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

	status_filter = request.GET.get("status", "").strip()
	sport_filter = request.GET.get("sport", "").strip()
	press_releases = PressRelease.objects.all()
	if status_filter:
		press_releases = press_releases.filter(status=status_filter)
	if sport_filter:
		press_releases = press_releases.filter(sport__icontains=sport_filter)
	return render(
		request,
		"media/press.html",
		{
			"press_releases": press_releases,
			"status_filter": status_filter,
			"sport_filter": sport_filter,
		},
	)


@role_required("media")
def export_press_csv(request):
	response = HttpResponse(content_type="text/csv")
	response["Content-Disposition"] = 'attachment; filename="press_releases.csv"'
	writer = csv.writer(response)
	writer.writerow(["Sport", "Headline", "Status", "Created"])
	for item in PressRelease.objects.all():
		writer.writerow([item.sport, item.headline, item.status, item.created_at])
	return response
