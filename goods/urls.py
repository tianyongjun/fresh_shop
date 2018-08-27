
from django.urls import path

from goods import views

urlpatterns = [
    # 首页
    path('goods_list/', views.GoodsList.as_view(), name='goods_list'),
    # 商品添加和编辑
    path('goods_detail/', views.GoodsDetail.as_view(), name='goods_detail'),
    # 删除商品
    path('goods_delete/<int:id>/', views.GoodsDelete.as_view(), name='goods_delete'),
    # 编辑商品的详情信息
    path('goods_desc/<int:id>/', views.GoodsDesc.as_view(), name='goods_desc')
]
