from django.contrib import admin
from .models import Fcuser
# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')  # 어떤 필드들을 list up 할 지


admin.site.register(Fcuser, FcuserAdmin)
