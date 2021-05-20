from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import Fcuser
from .forms import LoginForm

# Create your views here.


def home(request):
    return render(request, 'home.html')


def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass

    return redirect('/')


def login(request):
    # if request.method == 'GET':
    #     return render(request, 'login.html')
    # elif request.method == 'POST':
    #     username = request.POST.get('username', None)
    #     password = request.POST.get('password', None)

    #     res_data = {}
    #     if not (username and password):
    #         res_data['error'] = '모든 값을 입력해야합니다.'
    #     else:
    #         try:
    #             fcuser = Fcuser.objects.get(username=username)
    #             if check_password(password, fcuser.password):
    #                 request.session['user'] = fcuser.id
    #                 return redirect('/')
    #             else:
    #                 res_data['error'] = '비밀번호가 틀렸습니다.'
    #         except Fcuser.DoesNotExist:
    #             res_data['error'] = '존재하지 않는 아이디입니다.'
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        res_data = {}

        if not (username and password and re_password and useremail):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            fcuser = Fcuser(
                username=username,
                useremail=useremail,
                password=make_password(password),
            )
            fcuser.save()
            return redirect('/')
        return render(request, 'register.html', res_data)
