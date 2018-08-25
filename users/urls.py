
from django.urls import path

from users import views

urlpatterns = [
    # 登录
    path('login/', views.Login.as_view(), name='login'),
    # 注册
    path('register/', views.Register.as_view(), name='register'),
]
