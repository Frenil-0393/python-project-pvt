from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(role: str):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if getattr(request.user, "role", None) != role:
                return redirect("login")
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
