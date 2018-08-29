from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from goods.models import Goods
from shopping.models import ShoppingCart
from users.models import UserTicket
from utils.functions import is_login


class AddCart(View):
    def post(self, request, *args, **kwargs):
        """
        添加商品到购物车，使用session进行缓存。
        如果用户没有登录，则把商品添加到session中
        如果用户登录，则把商品同步到购物车表中
        """
        # 获取商品的ID和商品个数
        goods_id = request.POST.get('goods_id')
        goods_num = request.POST.get('goods_num')
        # 存入session中的商品的格式['商品id', '商品数量']
        goods_list = [goods_id, goods_num]
        # 判断session中用户的登录状态，如果第一次访问session，则设置登录状态为False
        if not request.session.get('login_status'):
            request.session['login_status'] = False

        cart_goods_num = 0
        # 首先判断session中是否有goods商品信息
        if request.session.get('goods'):
            # 如果session中存在购物车的商品信息，则先判断该商品是否在session中，如果在session中，则直接修改该商品的个数
            # 如果该商品不在session中，则直接添加进入session中
            # 使用flag标识，如果添加的商品已经存在session中，那么flag修改为1
            flag = 0
            for session_goods in request.session['goods']:
                if session_goods[0] == goods_id:
                    session_goods[1] = int(session_goods[1]) + int(goods_num)
                    flag = 1
            # 如果flag为0，则说明在session中没有添加过该商品，则直接使用append添加
            if not flag:
                goods = request.session['goods']
                goods.append(goods_list)
                request.session['goods'] = goods
            cart_goods_num = len(request.session['goods'])
        else:
            # 如果session中没有商品的信息，则首次添加商品的信息到session中，存入格式为列表
            goods = []
            goods.append(goods_list)
            request.session['goods'] = goods
            cart_goods_num = 1

        return JsonResponse({'code': 200, 'msg': '请求成功', 'cart_goods_num': cart_goods_num})


class Cart(View):
    def get(self, request, *args, **kwargs):
        # 购物车页面不用区分是否登录了商城，只用在下单的时候，进行判断用户是否登录即可
        # 下单的时候，判断如果没有登录，则跳转到登录页面。如果登录了，则直接跳转到支付页面

        # 先判断用户是否登录，如果登录则从数据库的购物车表中拿数据,如果登录状态验证失败，则从session中拿数据
        if request.session.get('login_status'):
            user = is_login(request)
            if user:
                shop_carts = ShoppingCart.objects.filter(user=user)
                return render(request, 'web/cart.html', {'shop_carts': shop_carts})
        # 从session中拿商品的id
        goods = request.session.get('goods')
        shop_carts = []
        if goods:
            # 如果session中存在已加入的商品，则获取商品的id
            goods_id = [good[0] for good in goods]
            shop_carts = ShoppingCart.objects.filter(goods_id__in=goods_id)

        return render(request, 'web/cart.html', {'shop_carts': shop_carts})


class ChangeSessionGoods(View):
    def post(self, request, *args, **kwargs):
        # 获取商品的ID和商品个数
        goods_id = request.POST.get('goods_id')
        goods_num = request.POST.get('goods_num')

        # 购物车中的商品有可能不存在session中，只存在于数据表中，则分两次中情况进行修改
        # 从session中拿商品的信息，并修改商品数量
        goods = request.session.get('goods')
        for session_goods in goods:
            if session_goods[0] == goods_id:
                session_goods[1] = int(session_goods[1]) + int(goods_num)
        # 从购物车表中直接修改商品个数
        user = is_login(request)
        if user:
            shop_cart = ShoppingCart.objects.filter(user=user, goods_id=goods_id).first()
            shop_cart.nums = goods_num
            shop_cart.save()
        return JsonResponse({'code': 200, 'msg': '请求成功'})


class TotalPrice(View):

    def get(self, request, *args, **kwargs):
        # 计算购物中商品的总价格，需要判断用户是否登录。
        # 如果用户没有登录，则总价格就是从session中获取商品去计算总价
        # 如果用户登录了，则总价格从数据库表中获取商品去计算总价

        if request.session.get('login_status'):
            user = is_login(request)
            if user:
                # 选择当前登录用户，勾选的商品，用于计算价格总和
                shop_carts = ShoppingCart.objects.filter(user=user, is_select=True)
                count = 0
                for shop_cart in shop_carts:
                    count += int(shop_cart.goods.shop_price) * int(shop_cart.nums)
                return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})

        # 从session中拿商品的id
        goods = request.session.get('goods')
        count = 0
        if goods:
            # 如果session中存在已加入的商品，则获取商品的id
            goods_id = [good[0] for good in goods]
            shop_carts = ShoppingCart.objects.filter(goods_id__in=goods_id, is_select=True)
            for shop_cart in shop_carts:
                count += int(shop_cart.goods.shop_price) * int(shop_cart.nums)
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


class ChangeCartGoodsSelect(View):

    def post(self, request, *args, **kwargs):
        # 修改购物车中商品的勾选状态
        cart_id = request.POST.get('cart_id')
        # 判断是否登录，如果登录，则修改购物车中商品的勾选状态
        if request.session.get('login_status'):
            # 通过购物车的id获取购物车数据
            shop_cart = ShoppingCart.objects.filter(id=cart_id).first()
            # 如果购物车中该商品的勾选状态为true则设置为false即可
            if shop_cart.is_select:
                shop_cart.is_select = False
            else:
                shop_cart.is_select = True
            shop_cart.save()
        return JsonResponse({'code': 200, 'msg': '请求成功'})

