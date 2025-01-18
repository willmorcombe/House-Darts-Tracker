from django.shortcuts import redirect
from django.urls import reverse


def login_required(function):

    def wrapper(request, *args, **kwargs):
        # Check session
        if request.session.get('username') is not None:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))
    
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper
