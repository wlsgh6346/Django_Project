from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import RegisterForm
from django.utils.decorators import method_decorator
from django.db import transaction
from user.decorators import login_required
from .models import Order
from product.models import Product
from user.models import User


# Create your views here.


@method_decorator(login_required, name="dispatch")
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        # with 안의 모든 처리는 transtion으로 처리됨 - 아주 개꿀임
        with transaction.atomic():
            good = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity=form.data.get('quantity'),
                product=good,
                user=User.objects.get(email=self.request.session.get('user'))
            )
            order.save()
            good.stock -= int(form.data.get('quantity'))
            good.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))

    # FormView에 존재하는 함수 - 어떤 인자 값을 전달해서 만들지 결정하는 함수 - request를 넣어줘야 함
    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({'request': self.request})
        return kw


@method_decorator(login_required, name="dispatch")
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        print(self.request.session.get('user'))
        queryset = Order.objects.filter(user__email=self.request.session.get('user'))
        return queryset
