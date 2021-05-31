from django.db import models
# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=128,
                             verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    writer = models.ForeignKey('user.user', verbose_name='작성자', on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='등록시간')
    password = models.CharField(max_length=64,
                                verbose_name='비밀번호')
    file_path = models.CharField(max_length=255, verbose_name='첨부 파일')
    file = models.FileField(null=True, blank=True, verbose_name='파일')
    # class를 반환하지 말고 안에 username을 반환하게 변경 fcuser object -> username이 나오게 됨

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'board'
        verbose_name = '게시글'  # 단수형
        verbose_name_plural = '게시글'  # 복수형
