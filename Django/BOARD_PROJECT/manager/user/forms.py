from django import forms
from django.contrib.auth.hashers import check_password
from .models import User


class RegisterForm(forms.Form):
    user_id = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요',
            'max_length': '8자리까지만 입력가능합니다.'
        },
        label='아이디', max_length=8
    )
    name = forms.CharField(
        error_messages={
            'required': '이름을 입력해주세요',
            'max_length': '10자리까지만 입력가능합니다.'
        },
        label='이름', max_length=10
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요',
            'max_length': '4자리까지만 입력가능합니다.'
        },
        widget=forms.PasswordInput, label='비밀번호',  max_length=4
    )
    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        try:
            User.objects.get(user_id=user_id)
            self.add_error('user_id', '이미 가입된 아이디입니다.')
        except User.DoesNotExist:
            pass

        if password and re_password:
            if password != re_password:
                self.add_error('re_password', '비밀번호를 확인하시기 바랍니다.')


class LoginForm(forms.Form):
    user_id = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요',
            'max_length': '8자리까지만 입력가능합니다.'
        },
        label='아이디', max_length=8
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요',
            'max_length': '4자리까지만 입력가능합니다.'
        },
        widget=forms.PasswordInput, label='비밀번호', max_length=4
    )

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if password and user_id:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 없습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀립니다.')
