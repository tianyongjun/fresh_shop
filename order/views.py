from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from fresh_shop.settings import PAGE_NUMBER
from order.models import OrderInfo, OrderGoods
from shopping.models import ShoppingCart
from users.models import UserAddress
from utils.functions import get_order_sn


class Order(View):

    def get(self, request, *args, **kwargs):
        # 获取当前登录系统的用户，该地址经过中间件处理，如果没有登录则直接跳转到登录页面
        user = request.user
        # 获取当前用户在购物车中勾选了的商品，并计算添加每一个商品的价格总和count字段
        shop_carts = ShoppingCart.objects.filter(user=user, is_select=True)
        for shop_cart in shop_carts:
            shop_cart.count = shop_cart.nums * shop_cart.goods.shop_price
        # 获取订单地址
        addresses = UserAddress.objects.filter(user=user)
        return render(request, 'web/place_order.html', {'shop_carts': shop_carts, 'addresses': addresses})

    def post(self, request, *args, **kwargs):
        # 下单
        user = request.user
        # 获取收货人的地址id
        address_id = request.POST.get('address_id')
        user_address = UserAddress.objects.filter(id=address_id).first()
        # 获取随机生成的订单号
        order_sn = get_order_sn()
        # 计算下单的商品的价格总和
        order_mount = 0
        order_goods_id = []
        shop_carts = ShoppingCart.objects.filter(user=user, is_select=True)
        for shop_cart in shop_carts:
            order_goods_id.append(shop_cart.goods_id)
            order_mount += shop_cart.nums * shop_cart.goods.shop_price
        # 创建订单
        order_info = OrderInfo.objects.create(user=user,order_sn=order_sn,
                                              order_mount=order_mount, address=user_address.address,
                                              signer_name=user_address.signer_name, signer_mobile=user_address.signer_mobile)
        # 创建订单和商品之间的详情关系
        for cart in shop_carts:
            OrderGoods.objects.create(order=order_info, goods=cart.goods, goods_nums=cart.nums)

        # 下单成功后，删除购物车中已下单的商品
        shop_carts.delete()
        # 下单成功后，删除session中已经下单的商品
        session_goods = request.session.get('goods')
        if session_goods:
            # 如果session中有缓存的商品信息，则for循环判断session中的商品是否已经下单
            # 如果已经下单，则删除session中该商品的信息
            session_goods_new = session_goods
            for o_goods_id in order_goods_id:
                for s_goods in session_goods:
                    # 判断如果session中商品的id存在于已经下单的商品中，则remove
                    if int(s_goods[0]) == o_goods_id:
                        session_goods_new.remove(s_goods)
        request.session['goods'] = session_goods_new

        return JsonResponse({'code': 200, 'msg': '请求成功'})


class UserOrder(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        # 获取分页
        try:
            # 如果page参数不能转化为int类型，则异常，默认page为1
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        # 获取当前用户所有的订单信息
        order_info = OrderInfo.objects.filter(user=user)
        paginator = Paginator(order_info, PAGE_NUMBER)
        order_info = paginator.page(page)
        order_status = OrderInfo.ORDER_STATUS
        return render(request, 'web/user_center_order.html', {'order_info': order_info, 'order_status': order_status})


class UserOrderSite(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_addresses = UserAddress.objects.filter(user=user).order_by('-id')

        return render(request, 'web/user_center_site.html', {'user_addresses': user_addresses})

