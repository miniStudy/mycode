from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def teacher_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'fac_logged_in' not in request.session:
            messages.error(request, "Login Required")
            return redirect('teacher_login')
        return view_func(request, *args, **kwargs)
    return wrapper
