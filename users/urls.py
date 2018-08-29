
from django.urls import path

from users import views

urlpatterns = [
    # 登录
    path('login/', views.Login.as_view(), name='login'),
    # 注册
    path('register/', views.Register.as_view(), name='register'),
    # 退出
    path('logout/', views.Logout.as_view(), name='logout'),
    # 登录验证，获取登录系统的用户
    path('is_login/', views.IsLogin.as_view(), name='is_login'),
]
