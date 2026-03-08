from django.shortcuts import render
from django.core.paginator import Paginator

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
	sort = request.GET.get("sort", "-created_at").strip() or "-created_at"
	live_matches = Match.objects.filter(status=Match.STATUS_LIVE)
	if sport:
		live_matches = live_matches.filter(sport__icontains=sport)
	updates = ScoreUpdate.objects.select_related("match").order_by(sort)
	if sport:
		updates = updates.filter(match__sport__icontains=sport)
	paginator = Paginator(updates, 10)
	page_obj = paginator.get_page(request.GET.get("page"))
	return render(
		request,
		"fan/live_scores.html",
		{
			"live_matches": live_matches,
			"updates": page_obj,
			"sport": sport,
			"sort": sort,
		},
	)


@role_required("fan")
def stats_view(request):
	metric = request.GET.get("metric", "").strip()
	team = request.GET.get("team", "").strip()
	sort = request.GET.get("sort", "player_name").strip() or "player_name"
	stats = PlayerStat.objects.select_related("match").all()
	if metric:
		stats = stats.filter(metric_name__icontains=metric)
	if team:
		stats = stats.filter(team_name__icontains=team)
	stats = stats.order_by(sort)
	paginator = Paginator(stats, 10)
	page_obj = paginator.get_page(request.GET.get("page"))
	return render(
		request,
		"fan/stats.html",
		{"stats": page_obj, "metric": metric, "team": team, "sort": sort},
	)


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
	sort = request.GET.get("sort", "-published_at").strip() or "-published_at"
	highlights = Highlight.objects.select_related("match").order_by(sort)
	paginator = Paginator(highlights, 10)
	page_obj = paginator.get_page(request.GET.get("page"))
	return render(request, "fan/highlights.html", {"highlights": page_obj, "sort": sort})
