from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .models import User


def _redirect_by_role(role: str):
	if role == User.ROLE_FAN:
		return redirect("fan:dashboard")
	if role == User.ROLE_ORGANIZER:
		return redirect("organizer:dashboard")
	return redirect("media:dashboard")


def login_view(request):
	if request.user.is_authenticated:
		return _redirect_by_role(request.user.role)

	if request.method == "POST":
		username = request.POST.get("username", "").strip()
		password = request.POST.get("password", "")
		role = request.POST.get("role", "")

		user = authenticate(request, username=username, password=password)
		if not user:
			messages.error(request, "Invalid username or password.")
			return render(request, "auth/login.html")

		if user.role != role:
			messages.error(request, "Selected role does not match your account.")
			return render(request, "auth/login.html")

		login(request, user)
		return _redirect_by_role(user.role)

	return render(request, "auth/login.html")


def register_view(request):
	if request.user.is_authenticated:
		return _redirect_by_role(request.user.role)

	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Registration successful. Please login.")
			return redirect("login")
		return render(request, "auth/register.html", {"form": form})

	return render(request, "auth/register.html", {"form": RegistrationForm()})


def logout_view(request):
	logout(request)
	return redirect("login")


@login_required
def profile_view(request):
	if request.method == "POST":
		full_name = request.POST.get("full_name", "").strip()
		email = request.POST.get("email", "").strip()
		if not full_name or not email:
			messages.error(request, "Name and email are required.")
			return redirect("profile")

		request.user.first_name = full_name
		request.user.email = email
		request.user.save(update_fields=["first_name", "email"])
		messages.success(request, "Profile updated successfully.")
		return redirect("profile")

	return render(request, "auth/profile.html")


@login_required
def change_password_view(request):
	if request.method == "POST":
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, "Password changed successfully.")
			return redirect("profile")
		messages.error(request, "Please correct the password form errors.")
		return render(request, "auth/change_password.html", {"form": form})

	form = PasswordChangeForm(request.user)
	return render(request, "auth/change_password.html", {"form": form})
