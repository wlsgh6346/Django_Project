from django.db import models
from user.models import User
import os
# Create your models here.

class BoardFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    
    def filename(self):
        return os.path.basename(self.file.name)
    
class Board(models.Model):
    title = models.CharField(max_length=128,
                             verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    writer = models.ForeignKey('user.user', verbose_name='작성자', on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='등록시간')
    files = models.ManyToManyField(BoardFile)
    
    hit = models.PositiveIntegerField(default=0, verbose_name='조회수')
    like_users = models.ManyToManyField(User, related_name="like_boards", blank=True)
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    # class를 반환하지 말고 안에 username을 반환하게 변경 fcuser object -> username이 나오게 됨

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'board'
        verbose_name = '게시글'  # 단수형
        verbose_name_plural = '게시글'  # 복수형



class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    board = models.ForeignKey('Board', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
