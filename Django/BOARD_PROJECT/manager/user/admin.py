from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password')  # 어떤 필드들을 list up 할 지


admin.site.register(User, UserAdmin)
