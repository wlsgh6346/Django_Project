from django.db import models

# Create your models here.


class Fcuser(models.Model):
    username = models.CharField(max_length=32,
                                verbose_name='사용자명')
    useremail = models.EmailField(max_length=128,
                                  verbose_name='사용자이메일')
    password = models.CharField(max_length=64,
                                verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')

    # class를 반환하지 말고 안에 username을 반환하게 변경 fcuser object -> username이 나오게 됨
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'fcuser'
        verbose_name = '게시판 사용자'  # 단수형
        verbose_name_plural = '게시판 사용자'  # 복수형
