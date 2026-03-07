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
	metric = request.GET.get("metric", "").strip()
	team = request.GET.get("team", "").strip()
	stats = PlayerStat.objects.select_related("match").all()
	if metric:
		stats = stats.filter(metric_name__icontains=metric)
	if team:
		stats = stats.filter(team_name__icontains=team)
	return render(request, "fan/stats.html", {"stats": stats, "metric": metric, "team": team})


@role_required("fan")
def leaderboard_view(request):
	metric = request.GET.get("metric", "runs").strip() or "runs"
	stats = (
		PlayerStat.objects.filter(metric_name__icontains=metric)
		.select_related("match")
		.order_by("-metric_value", "player_name")
	)
	return render(request, "fan/leaderboard.html", {"stats": stats, "metric": metric})


@role_required("fan")
def highlights_view(request):
	highlights = Highlight.objects.select_related("match").all()
	return render(request, "fan/highlights.html", {"highlights": highlights})
