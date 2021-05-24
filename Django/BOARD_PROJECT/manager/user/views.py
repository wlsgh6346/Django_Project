from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from .models import User
# Create your views here.


def index(request):

    return render(request, "index.html")


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            user_id=form.data.get('user_id'),
            name=form.data.get('name'),
            password=make_password(form.data.get('password')),

        )
        user.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def get_initial(self):
        initial = super(LoginView, self).get_initial()
        initial.update({'user_id': self.request.session.get('user_id', '')})

        return initial

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('user_id')

        if form.data.get('auto_login'):
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

        if form.data.get('save_id'):
            self.request.session['user_id'] = form.data.get('user_id')
        else:
            if self.request.session['user_id']:
                del(self.request.session['user_id'])

        return super().form_valid(form)


def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')
