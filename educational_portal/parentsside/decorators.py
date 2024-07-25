from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def parent_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'parent_logged_in' not in request.session:
            messages.error(request, "<div class='bg-danger text-white p-2 rounded-2 returnmessage mb-2' id='returnmessage'><i class='fa-solid fa-triangle-exclamation me-2'></i> Login Required.</div>")
            return redirect('parent_login')
        return view_func(request, *args, **kwargs)
    return wrapper
