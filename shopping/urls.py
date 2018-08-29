
from django.urls import path

from shopping import views

urlpatterns = [
    # 添加商品到购物车中
    path('add_cart/', views.AddCart.as_view(), name='add_cart'),
    # 购物车
    path('cart/', views.Cart.as_view(), name='cart'),
]
