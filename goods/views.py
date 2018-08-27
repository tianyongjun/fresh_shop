from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from goods.forms import GoodsForm
from goods.models import GoodsCategory, Goods


class GoodsList(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回首页
        goods = Goods.objects.all()
        goods_categorys = GoodsCategory.CATEGORY_TYPE
        return render(request, 'backweb/goods_list.html', {'goods': goods, 'goods_categorys': goods_categorys})


class GoodsDetail(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回首页
        goods_categorys = GoodsCategory.CATEGORY_TYPE
        return render(request, 'backweb/goods_detail.html', {'goods_categorys': goods_categorys})

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = GoodsForm(data, request.FILES)
        # 验证商品表单数据是否填写正确
        if form.is_valid():
            # 创建商品信息
            goods_data = form.cleaned_data
            Goods.objects.create(**goods_data)
            # 创建成功，则跳回商品列表页面
            return redirect('goods:goods_list')
        else:
            # 如果验证商品表单数据不成功，则返回商品添加页面，并且返回错误信息
            return render(request, 'backweb/goods_detail.html', {'form': form, 'data': data})


class GoodsDelete(View):
    def post(self, request, *args, **kwargs):
        # 获取删除的商品id，查询数据，使用delete()方法删除
        Goods.objects.filter(id=kwargs['id']).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})


class GoodsDesc(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'backweb/goods_desc.html')

    def post(self, request, *args, **kwargs):
        # 获取删除的商品id，查询数据，使用delete()方法删除
        content = request.POST.get('content')
        goods = Goods.objects.filter(id=kwargs['id']).first()
        goods.goods_desc = content
        goods.save()
        return redirect('goods:goods_list')
