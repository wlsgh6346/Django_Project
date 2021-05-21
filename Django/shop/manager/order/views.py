from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm
# Create your views here.


class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))

    # FormView에 존재하는 함수 - 어떤 인자 값을 전달해서 만들지 결정하는 함수 - request를 넣어줘야 함
    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({'request': self.request})
        return kw
