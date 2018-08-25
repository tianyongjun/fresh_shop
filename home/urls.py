
from django.urls import path

from home import views

urlpatterns = [
    # 首页
    path('index/', views.Index.as_view(), name='index'),
]
