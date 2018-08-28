
from django.urls import path

from goods import views

urlpatterns = [
    # 商品列表页面
    path('goods_list/', views.GoodsList.as_view(), name='goods_list'),
    # 商品添加
    path('goods_detail/', views.GoodsDetail.as_view(), name='goods_detail'),
    # 商品编辑
    path('goods_edit/<int:id>/', views.GoodsEdit.as_view(), name='goods_edit'),
    # 删除商品
    path('goods_delete/<int:id>/', views.GoodsDelete.as_view(), name='goods_delete'),
    # 编辑商品的详情信息
    path('goods_desc/<int:id>/', views.GoodsDesc.as_view(), name='goods_desc'),
    # 商品分类列表
    path('goods_category_list/', views.GoodsCategoryList.as_view(), name='goods_category_list'),
    # 商品分类删除
    path('goods_category_editor/<int:id>/', views.GoodsCategoryEditor.as_view(), name='goods_category_editor'),

]
