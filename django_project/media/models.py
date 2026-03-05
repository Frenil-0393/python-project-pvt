from django.db import models

from organizer.models import Match


class BroadcastSession(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="broadcasts")
	channel_name = models.CharField(max_length=120)
	stream_url = models.URLField(blank=True)
	is_live = models.BooleanField(default=False)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]

	def __str__(self):
		return f"{self.channel_name} - {self.match}"


class Highlight(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="highlights")
	title = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	duration = models.CharField(max_length=20, blank=True)
	views = models.PositiveIntegerField(default=0)
	published_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-published_at"]

	def __str__(self):
		return self.title


class PressRelease(models.Model):
	STATUS_DRAFT = "draft"
	STATUS_PUBLISHED = "published"
	STATUS_CHOICES = [
		(STATUS_DRAFT, "Draft"),
		(STATUS_PUBLISHED, "Published"),
	]

	sport = models.CharField(max_length=80)
	headline = models.CharField(max_length=200)
	body = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return self.headline
