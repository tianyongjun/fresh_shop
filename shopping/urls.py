
from django.urls import path

from shopping import views

urlpatterns = [
    # 添加商品到购物车中
    path('add_cart/', views.AddCart.as_view(), name='add_cart'),
    # 购物车
    path('cart/', views.Cart.as_view(), name='cart'),
    # 修改购物车中数据
    path('change_session_goods/', views.ChangeSessionGoods.as_view(), name='change_session_goods'),
    # 购物车中计算商品的总价
    path('total_price/', views.TotalPrice.as_view(), name='total_price'),
    # 购物车中商品的勾选状态
    path('change_cart_goods_select/', views.ChangeCartGoodsSelect.as_view(), name='change_cart_goods_select'),

]
