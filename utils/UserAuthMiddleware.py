
import re
from datetime import datetime

from django.db.models import Q
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from shopping.models import ShoppingCart
from users.models import UserTicket


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 不需要验证url地址
        not_need_login = ['/home/index/', '/goods/goods_detail/(.*)','/users/login/',
                          '/users/register/', '/media/(.*)', '/static/(.*)',
                          '/shopping/add_cart/', '/shopping/cart/']
        # 获取当前访问url的地址
        path = request.path
        # 当访问首页的时候，不需要做登录验证的处理
        if path == '/':
            return None

        # 判断如果请求地址为不需要登录验证的地址，则返回None
        for not_need_path in not_need_login:
            if re.match(not_need_path, path):
               return None

        # 先获取cookies中的ticket参数
        ticket = request.COOKIES.get('ticket')
        # 如果没有ticket，则直接跳转到登录
        if not ticket:
            return redirect('users:login')

        user_ticket = UserTicket.objects.filter(ticket=ticket).first()
        if user_ticket:
            # 获取到有认证的相关信息
            # 1. 验证当前认证信息是否过期，如果没过期，request.user赋值
            # 2. 如果过期了，跳转到登录，并删除认证信息
            if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                # 过期
                UserTicket.objects.filter(user=user_ticket.user).delete()
                return redirect('users:login')
            else:
                # 没有过期，赋值request.user，并且删除多余的认证信息
                request.user = user_ticket.user
                return None
        else:
            return redirect('users:login')


class AuthSessionMiddleware(MiddlewareMixin):
    """
    用户的session状态验证
    """
    def process_request(self, request):

        if request.session.get('login_status'):
            # 如果从session中获取到用户的登录状态为True，则同步session中的数据到数据库的购物车表模型中
            # 获取当前登录系统的用户
            user = request.user
            # 如果获取到当前登录系统的用户，则同步session中的数据到数据库中
            if user.id:
                session_goods = request.session.get('goods')
                if session_goods:
                    # 循环执行同步session数据到数据库，其中goods为列表['商品的id','商品的数量']
                    for goods in session_goods:
                        shop_cart = ShoppingCart.objects.filter(goods_id=goods[0], user=user).first()
                        if not shop_cart:
                            # 如果购物车中没有该用户对应的商品信息，则创建
                            ShoppingCart.objects.create(goods_id=goods[0], nums=goods[1], user=user)
                        else:
                            # 如果购物车中有该用户对应的商品信息，则判断商品个数是否变化，变化则更新
                            if shop_cart.nums != goods[1]:
                                shop_cart.nums == goods[1]
                                shop_cart.save()
        return None
