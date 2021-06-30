from urllib.parse import urlparse
from django.shortcuts import redirect
from django.contrib import messages
from .models import User


def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            user_attr = getattr(request, 'user')
            path = urlparse(request.META['HTTP_REFERER']).path
            return redirect('/login/?next='+path)
        return function(request, *args, **kwargs)
    return wrap
