from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
