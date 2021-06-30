from django.shortcuts import redirect, render, HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from .models import User
from .helper import email_auth_num, send_mail
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):

    return render(request, "index.html")


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'
    
    def get_initial(self):
        init = super(RegisterView, self).get_initial()
        init.update({'request':self.request})
        return init
    
    def form_valid(self, form):
        
        
        email_front = form.data.get('email_1')
        email_end = self.request.POST.get('email_2')
        email = email_front+"@"+email_end
        user = User(
            user_id=form.data.get('user_id'),
            name=form.data.get('name'),
            password=make_password(form.data.get('password')),
            email=email,
        )
        user.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        next = self.request.POST.get('next')
        return next

    def get_initial(self):
        path = self.request.GET.get('next', '/')
        initial = super(LoginView, self).get_initial()
        print(path)
        initial.update({
            'user_id': self.request.session.get('user_id', ''),
            'path': path
        })
        return initial

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('user_id')

        if form.data.get('auto_login'):
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

        if form.data.get('save_id'):
            self.request.session['user_id'] = form.data.get('user_id')
        else:
            if self.request.session.get('user_id', ''):
                del(self.request.session['user_id'])

        return super().form_valid(form)


def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')

@csrf_exempt
def ajax_send_auth_email(request):
    auth_num = email_auth_num()
    email = request.POST.get('email')
    request.session['auth_email'] = auth_num
    send_mail(
        '이메일 인증 번호',
        [email],
        html=render_to_string('recovery_email.html', {
                'auth_num': auth_num,
            }),
    )
    return HttpResponse(json.dumps({'result': 'success'}), content_type="application/json")

    