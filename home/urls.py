
from django.urls import path

from home import views

urlpatterns = [
    # 首页
    path('index/', views.Index.as_view(), name='index'),
    # 商品详情
    path('goods_detail/<int:id>/', views.GoodsDetail.as_view(), name='goods_detail'),
]
