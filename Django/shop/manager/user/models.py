from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    # 각 model을 문자열로 변환했을 때 보여지는 설정
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
