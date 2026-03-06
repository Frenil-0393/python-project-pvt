from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from common.decorators import role_required
from organizer.models import Match, PlayerStat, ScoreUpdate


@role_required("organizer")
def dashboard(request):
	return render(request, "organizer/dashboard.html", {"user_name": request.user.first_name or "Organizer"})


@role_required("organizer")
def schedule_view(request):
	if request.method == "POST":
		action = request.POST.get("action", "create")
		if action == "delete":
			match_id = request.POST.get("match_id")
			deleted, _ = Match.objects.filter(id=match_id).delete()
			if deleted:
				messages.success(request, "Match deleted.")
			else:
				messages.error(request, "Match not found.")
			return redirect("organizer:schedule")

		sport = request.POST.get("sport", "").strip()
		home_team = request.POST.get("home_team", "").strip()
		away_team = request.POST.get("away_team", "").strip()
		venue = request.POST.get("venue", "").strip()
		start_time_raw = request.POST.get("start_time", "").strip()
		status = request.POST.get("status", Match.STATUS_SCHEDULED)

		if not all([sport, home_team, away_team, venue, start_time_raw]):
			messages.error(request, "Please fill all match fields.")
			return redirect("organizer:schedule")

		try:
			start_time = timezone.datetime.fromisoformat(start_time_raw)
		except ValueError:
			messages.error(request, "Invalid date/time format.")
			return redirect("organizer:schedule")

		Match.objects.create(
			sport=sport,
			home_team=home_team,
			away_team=away_team,
			venue=venue,
			start_time=start_time,
			status=status,
		)
		messages.success(request, "Match fixture created.")
		return redirect("organizer:schedule")

	matches = Match.objects.all()
	return render(request, "organizer/schedule.html", {"matches": matches})


@role_required("organizer")
def scores_view(request):
	if request.method == "POST":
		action = request.POST.get("action", "create")
		if action == "delete":
			update_id = request.POST.get("update_id")
			deleted, _ = ScoreUpdate.objects.filter(id=update_id).delete()
			if deleted:
				messages.success(request, "Score update deleted.")
			else:
				messages.error(request, "Score update not found.")
			return redirect("organizer:scores")

		match_id = request.POST.get("match_id")
		summary = request.POST.get("summary", "").strip()
		status_note = request.POST.get("status_note", "").strip()

		if not match_id or not summary:
			messages.error(request, "Please select a match and enter score summary.")
			return redirect("organizer:scores")

		match = Match.objects.filter(id=match_id).first()
		if not match:
			messages.error(request, "Invalid match selected.")
			return redirect("organizer:scores")

		latest = ScoreUpdate.objects.filter(match=match).first()
		if latest and latest.summary == summary and latest.status_note == status_note:
			messages.error(request, "No changes detected in score update.")
			return redirect("organizer:scores")

		ScoreUpdate.objects.create(match=match, summary=summary, status_note=status_note)
		messages.success(request, "Score updated successfully.")
		return redirect("organizer:scores")

	matches = Match.objects.all()
	score_updates = ScoreUpdate.objects.select_related("match").all()
	return render(
		request,
		"organizer/scores.html",
		{
			"matches": matches,
			"score_updates": score_updates,
		},
	)


@role_required("organizer")
def players_view(request):
	if request.method == "POST":
		action = request.POST.get("action", "create")
		if action == "delete":
			stat_id = request.POST.get("stat_id")
			deleted, _ = PlayerStat.objects.filter(id=stat_id).delete()
			if deleted:
				messages.success(request, "Player stat deleted.")
			else:
				messages.error(request, "Player stat not found.")
			return redirect("organizer:players")

		match_id = request.POST.get("match_id")
		player_name = request.POST.get("player_name", "").strip()
		team_name = request.POST.get("team_name", "").strip()
		metric_name = request.POST.get("metric_name", "").strip()
		metric_value = request.POST.get("metric_value", "").strip()
		availability = request.POST.get("availability", "").strip() or "Available"

		if not all([match_id, player_name, team_name, metric_name, metric_value]):
			messages.error(request, "Please fill all player stat fields.")
			return redirect("organizer:players")

		match = Match.objects.filter(id=match_id).first()
		if not match:
			messages.error(request, "Invalid match selected.")
			return redirect("organizer:players")

		PlayerStat.objects.create(
			match=match,
			player_name=player_name,
			team_name=team_name,
			metric_name=metric_name,
			metric_value=metric_value,
			availability=availability,
		)
		messages.success(request, "Player stats updated.")
		return redirect("organizer:players")

	matches = Match.objects.all()
	player_stats = PlayerStat.objects.select_related("match").all()
	return render(
		request,
		"organizer/players.html",
		{
			"matches": matches,
			"player_stats": player_stats,
		},
	)
