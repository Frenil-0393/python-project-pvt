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

	def test_profile_update(self):
		user = User.objects.create_user(
			username="orguser",
			password="StrongPass123",
			email="org@example.com",
			role="organizer",
			first_name="Old Name",
		)
		self.client.login(username="orguser", password="StrongPass123")
		response = self.client.post(
			reverse("profile"),
			{
				"full_name": "New Name",
				"email": "new@example.com",
			},
		)
		self.assertEqual(response.status_code, 302)
		user.refresh_from_db()
		self.assertEqual(user.first_name, "New Name")
		self.assertEqual(user.email, "new@example.com")

	def test_login_redirects_if_authenticated(self):
		User.objects.create_user(
			username="fan2",
			password="StrongPass123",
			email="fan2@example.com",
			role="fan",
		)
		self.client.login(username="fan2", password="StrongPass123")
		response = self.client.get(reverse("login"))
		self.assertEqual(response.status_code, 302)
		self.assertIn("/fan/", response.url)

	def test_change_password(self):
		User.objects.create_user(
			username="pwuser",
			password="StrongPass123",
			email="pw@example.com",
			role="media",
		)
		self.client.login(username="pwuser", password="StrongPass123")
		response = self.client.post(
			reverse("change_password"),
			{
				"old_password": "StrongPass123",
				"new_password1": "NewStrongPass456",
				"new_password2": "NewStrongPass456",
			},
		)
		self.assertEqual(response.status_code, 302)
		self.client.logout()
		relogin = self.client.login(username="pwuser", password="NewStrongPass456")
		self.assertTrue(relogin)

	def test_login_lockout_after_failed_attempts(self):
		User.objects.create_user(
			username="lockuser",
			password="StrongPass123",
			email="lock@example.com",
			role="fan",
		)
		for _ in range(5):
			self.client.post(
				reverse("login"),
				{
					"username": "lockuser",
					"password": "WrongPass",
					"role": "fan",
				},
			)

		response = self.client.post(
			reverse("login"),
			{
				"username": "lockuser",
				"password": "StrongPass123",
				"role": "fan",
			},
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Too many failed attempts")

	def test_register_duplicate_email_rejected(self):
		User.objects.create_user(
			username="existing",
			password="StrongPass123",
			email="same@example.com",
			role="fan",
		)
		response = self.client.post(
			reverse("register"),
			{
				"username": "newuser",
				"full_name": "New User",
				"email": "SAME@example.com",
				"role": "fan",
				"password1": "StrongPass123",
				"password2": "StrongPass123",
			},
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "already registered")
