
from django.urls import path

from pay import views

urlpatterns = [
    # 登录
    path('pay_order/', views.PayOrder.as_view(), name='pay_order'),
    # 校验支付状态是否成功
    path('check_pay_status/', views.CheckPayStatus.as_view(), name='check_pay_status'),

]
