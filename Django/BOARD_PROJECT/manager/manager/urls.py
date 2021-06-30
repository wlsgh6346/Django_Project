"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user.views import index, RegisterView, LoginView, logout, ajax_send_auth_email
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('board/detail/<int:pk>/', views.board_detail),
    path('board/list/', views.board_list),
    path('board/write/', views.board_write),
    path('board/update/<int:pk>/', views.board_update),
    path('board/delete/<int:pk>/', views.board_delete),
    path('board/like/<int:pk>/', views.like_board, name="like_board"),
    path('board/comment/', views.write_comment, name="write_comment"),
    path('board/delete_comment/<int:pk>', views.delete_comment, name="delete_comment"),
    path('board/board_delete_multi', views.board_delete_multi),
    path('ajax_send_auth_email/', ajax_send_auth_email, name="ajax_send_auth_email"),
    path('download_zip_file/<int:pk>', views.download_zip_file),
    path('board_test/',views.board_test)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
