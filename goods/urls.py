
from django.urls import path

from goods import views

urlpatterns = [
    # 商品详情
    path('goods_detail/<int:id>/', views.GoodsDetail.as_view(), name='goods_detail'),
]
