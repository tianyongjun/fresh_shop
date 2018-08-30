
from django.urls import path

from order import views

urlpatterns = [
    # 下单
    path('order/', views.Order.as_view(), name='order'),
    # 订单中心
    path('user_order/', views.UserOrder.as_view(), name='user_order'),
    # 收货地址
    path('user_order_site/', views.UserOrderSite.as_view(), name='user_order_site'),

]
