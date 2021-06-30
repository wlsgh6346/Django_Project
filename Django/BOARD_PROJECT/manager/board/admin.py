from django.contrib import admin
from .models import Board, Comment
# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)  # 어떤 필드들을 list up 할 지


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'board', 'created_at')  # 어떤 필드들을 list up 할 지


admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
