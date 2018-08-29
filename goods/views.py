
from django.shortcuts import render
from django.views import View

from goods.models import Goods


class GoodsDetail(View):
    def get(self, request, *args, **kwargs):
        # 获取商品详情信息
        goods = Goods.objects.filter(id=kwargs['id']).first()
        return render(request, 'web/detail.html', {'goods': goods})