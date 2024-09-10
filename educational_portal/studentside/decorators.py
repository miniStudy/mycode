from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def student_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'stud_logged_in' not in request.session:
            messages.error(request, "Login Required")
            return redirect('Student_Login')
        return view_func(request, *args, **kwargs)
    return wrapper
