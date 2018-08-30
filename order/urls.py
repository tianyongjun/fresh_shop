
from django.urls import path

from order import views

urlpatterns = [
    # 下单
    path('order/', views.Order.as_view(), name='order'),

]
