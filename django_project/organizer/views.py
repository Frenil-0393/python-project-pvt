from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db.models import Q
import csv

from common.decorators import role_required
from organizer.models import Match, PlayerStat, ScoreUpdate


@role_required("organizer")
def dashboard(request):
	context = {
		"user_name": request.user.first_name or "Organizer",
		"total_matches": Match.objects.count(),
		"live_matches": Match.objects.filter(status=Match.STATUS_LIVE).count(),
		"upcoming_matches": Match.objects.filter(status=Match.STATUS_SCHEDULED).count(),
		"total_score_updates": ScoreUpdate.objects.count(),
		"total_player_stats": PlayerStat.objects.count(),
	}
	return render(request, "organizer/dashboard.html", context)


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
		if action == "set_status":
			match_id = request.POST.get("match_id")
			status = request.POST.get("status", Match.STATUS_SCHEDULED)
			updated = Match.objects.filter(id=match_id).update(status=status)
			if updated:
				messages.success(request, "Match status updated.")
			else:
				messages.error(request, "Match not found.")
			return redirect("organizer:schedule")
		if action == "bulk_status":
			status = request.POST.get("status", Match.STATUS_SCHEDULED)
			ids = request.POST.getlist("match_ids")
			if not ids:
				messages.error(request, "Select at least one match for bulk update.")
				return redirect("organizer:schedule")
			updated = Match.objects.filter(id__in=ids).update(status=status)
			messages.success(request, f"Updated status for {updated} matches.")
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

		exists = Match.objects.filter(
			sport=sport,
			home_team=home_team,
			away_team=away_team,
			start_time=start_time,
		).exists()
		if exists:
			messages.error(request, "Duplicate fixture exists for same sport/teams/time.")
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

	sport = request.GET.get("sport", "").strip()
	status_filter = request.GET.get("status", "").strip()
	matches = Match.objects.all()
	if sport:
		matches = matches.filter(sport__icontains=sport)
	if status_filter:
		matches = matches.filter(status=status_filter)
	return render(
		request,
		"organizer/schedule.html",
		{"matches": matches, "sport": sport, "status_filter": status_filter},
	)


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

	match_search = request.GET.get("match", "").strip()
	matches = Match.objects.all()
	score_updates = ScoreUpdate.objects.select_related("match").all()
	if match_search:
		score_updates = score_updates.filter(
			Q(match__home_team__icontains=match_search) | Q(match__away_team__icontains=match_search)
		)
	return render(
		request,
		"organizer/scores.html",
		{
			"matches": matches,
			"score_updates": score_updates,
			"match_search": match_search,
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

		obj, created = PlayerStat.objects.update_or_create(
			match=match,
			player_name=player_name,
			metric_name=metric_name,
			defaults={
				"team_name": team_name,
				"metric_value": metric_value,
				"availability": availability,
			},
		)
		messages.success(request, "Player stat created." if created else "Player stat updated.")
		return redirect("organizer:players")

	team_filter = request.GET.get("team", "").strip()
	metric_filter = request.GET.get("metric", "").strip()
	matches = Match.objects.all()
	player_stats = PlayerStat.objects.select_related("match").all()
	if team_filter:
		player_stats = player_stats.filter(team_name__icontains=team_filter)
	if metric_filter:
		player_stats = player_stats.filter(metric_name__icontains=metric_filter)
	return render(
		request,
		"organizer/players.html",
		{
			"matches": matches,
			"player_stats": player_stats,
			"team_filter": team_filter,
			"metric_filter": metric_filter,
		},
	)


@role_required("organizer")
def export_matches_csv(request):
	response = HttpResponse(content_type="text/csv")
	response["Content-Disposition"] = 'attachment; filename="matches.csv"'
	writer = csv.writer(response)
	writer.writerow(["Sport", "Home Team", "Away Team", "Venue", "Start Time", "Status"])
	for item in Match.objects.all():
		writer.writerow([item.sport, item.home_team, item.away_team, item.venue, item.start_time, item.status])
	return response


@role_required("organizer")
def export_scores_csv(request):
	response = HttpResponse(content_type="text/csv")
	response["Content-Disposition"] = 'attachment; filename="scores.csv"'
	writer = csv.writer(response)
	writer.writerow(["Match", "Summary", "Status Note", "Created"])
	for item in ScoreUpdate.objects.select_related("match").all():
		writer.writerow([
			f"{item.match.home_team} vs {item.match.away_team}",
			item.summary,
			item.status_note,
			item.created_at,
		])
	return response


@role_required("organizer")
def export_players_csv(request):
	response = HttpResponse(content_type="text/csv")
	response["Content-Disposition"] = 'attachment; filename="player_stats.csv"'
	writer = csv.writer(response)
	writer.writerow(["Player", "Team", "Metric", "Value", "Availability", "Match"])
	for item in PlayerStat.objects.select_related("match").all():
		writer.writerow([
			item.player_name,
			item.team_name,
			item.metric_name,
			item.metric_value,
			item.availability,
			f"{item.match.home_team} vs {item.match.away_team}",
		])
	return response
