from product.models import Product
from django import forms
from .models import Order
from user.models import User
from django.db import transaction


class RegisterForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={'required': '수량을 입력해주세요.'},
        label='수량'
    )
    product = forms.IntegerField(
        error_messages={'required': '상품설명을 입력해주세요.'},
        label='상품설명', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        user = self.request.session.get('user', None)

        if quantity and product and user:
            # with 안의 모든 처리는 transtion으로 처리됨 - 아주 개꿀임
            with transaction.atomic():
                good = Product.objects.get(pk=product)
                order = Order(
                    quantity=quantity,
                    product=Product.objects.get(pk=product),
                    user=User.objects.get(email=user)
                )
                order.save()
                good.stock -= quantity
                good.save()

        else:
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')
