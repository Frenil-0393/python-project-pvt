from django.db import models


class Match(models.Model):
	STATUS_SCHEDULED = "scheduled"
	STATUS_LIVE = "live"
	STATUS_FINISHED = "finished"

	STATUS_CHOICES = [
		(STATUS_SCHEDULED, "Scheduled"),
		(STATUS_LIVE, "Live"),
		(STATUS_FINISHED, "Finished"),
	]

	sport = models.CharField(max_length=50)
	home_team = models.CharField(max_length=100)
	away_team = models.CharField(max_length=100)
	venue = models.CharField(max_length=150)
	start_time = models.DateTimeField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["start_time"]

	def __str__(self):
		return f"{self.sport}: {self.home_team} vs {self.away_team}"


class ScoreUpdate(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="score_updates")
	summary = models.CharField(max_length=200)
	status_note = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.match} -> {self.summary}"


class PlayerStat(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="player_stats")
	player_name = models.CharField(max_length=120)
	team_name = models.CharField(max_length=120)
	metric_name = models.CharField(max_length=80)
	metric_value = models.CharField(max_length=80)
	availability = models.CharField(max_length=80, default="Available")
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["player_name"]

	def __str__(self):
		return f"{self.player_name} ({self.metric_name}: {self.metric_value})"
