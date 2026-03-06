from django.shortcuts import render

from common.decorators import role_required
from media.models import Highlight
from organizer.models import Match, PlayerStat, ScoreUpdate


@role_required("fan")
def dashboard(request):
	return render(request, "fan/dashboard.html", {"user_name": request.user.first_name or "Fan"})


@role_required("fan")
def timetable_view(request):
	sport = request.GET.get("sport", "").strip()
	matches = Match.objects.all()
	if sport:
		matches = matches.filter(sport__icontains=sport)
	return render(request, "fan/timetable.html", {"matches": matches, "sport": sport})


@role_required("fan")
def live_scores_view(request):
	sport = request.GET.get("sport", "").strip()
	live_matches = Match.objects.filter(status=Match.STATUS_LIVE)
	if sport:
		live_matches = live_matches.filter(sport__icontains=sport)
	updates = ScoreUpdate.objects.select_related("match").all()
	if sport:
		updates = updates.filter(match__sport__icontains=sport)
	return render(
		request,
		"fan/live_scores.html",
		{
			"live_matches": live_matches,
			"updates": updates,
			"sport": sport,
		},
	)


@role_required("fan")
def stats_view(request):
	stats = PlayerStat.objects.select_related("match").all()
	return render(request, "fan/stats.html", {"stats": stats})


@role_required("fan")
def highlights_view(request):
	highlights = Highlight.objects.select_related("match").all()
	return render(request, "fan/highlights.html", {"highlights": highlights})
