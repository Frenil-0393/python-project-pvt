from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountsFlowTests(TestCase):
	def test_register_user(self):
		response = self.client.post(
			reverse("register"),
			{
				"username": "fanuser",
				"full_name": "Fan User",
				"email": "fan@example.com",
				"role": "fan",
				"password1": "StrongPass123",
				"password2": "StrongPass123",
			},
		)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(User.objects.filter(username="fanuser").exists())

	def test_login_with_role(self):
		User.objects.create_user(
			username="mediauser",
			password="StrongPass123",
			email="media@example.com",
			role="media",
		)
		response = self.client.post(
			reverse("login"),
			{
				"username": "mediauser",
				"password": "StrongPass123",
				"role": "media",
			},
		)
		self.assertEqual(response.status_code, 302)
		self.assertIn("/media/", response.url)
