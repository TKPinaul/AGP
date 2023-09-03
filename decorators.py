from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.title == 'Administrator':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return _wrapped_view

