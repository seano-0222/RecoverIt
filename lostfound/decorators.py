from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You don't have permission to access the admin dashboard.")
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return _wrapped