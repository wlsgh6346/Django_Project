from django.shortcuts import redirect
from django.contrib import messages
from .models import User


def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            messages.info(request, "로그인한 사용자만 이용할 수 있습니다.")
            return redirect('/login/')
        return function(request, *args, **kwargs)
    return wrap
