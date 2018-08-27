
from django.urls import path

from backweb import views

urlpatterns = [
    # 办理后台首页
    path('index/', views.Index.as_view(), name='index'),
]
