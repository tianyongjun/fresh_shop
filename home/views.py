
from django.shortcuts import render
from django.views import View

from goods.models import Goods, GoodsCategory


class Index(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回首页
        goods = Goods.objects.all().order_by('id')
        goods_all = {}
        goods_categorys = GoodsCategory.CATEGORY_TYPE
        for goods_type in goods_categorys:
            data = []
            # 用于统计每个分类下添加商品的个数
            count = 0
            for good in goods:
                # 判断商品的分类
                if good.category_id == goods_type[0]:
                    # 组装data列表，每一个商品分类下只有4个商品信息
                    if count < 5:
                        data.append(good)
                        count += 1
            goods_all['goods_' + str(goods_type[0])] = data
        return render(request, 'web/index.html', {'goods_all': goods_all, 'goods_categorys': goods_categorys})


class GoodsDetail(View):
    def get(self, request, *args, **kwargs):
        # 获取商品详情信息
        goods = Goods.objects.filter(id=kwargs['id']).first()
        return render(request, 'web/detail.html', {'goods': goods})

