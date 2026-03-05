from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	ROLE_FAN = "fan"
	ROLE_ORGANIZER = "organizer"
	ROLE_MEDIA = "media"

	ROLE_CHOICES = [
		(ROLE_FAN, "Sport Fan"),
		(ROLE_ORGANIZER, "Organizer"),
		(ROLE_MEDIA, "Media & Broadcast"),
	]

	role = models.CharField(max_length=20, choices=ROLE_CHOICES)
