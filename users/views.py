
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.forms import UserRegisterForm, UserLoginForm, UserAddressForm
from users.models import User, UserTicket, UserAddress
from utils.functions import get_random_ticket


class Login(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回登录页面
        return render(request, 'web/login.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = UserLoginForm(data)
        if form.is_valid():
            # 1. 验证表单成功，获取用户信息
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            # 如果验证用户名不正确，则返回登录页面
            if not user:
                return redirect('users:login')
            # 如果验证用户存在，但是密码错误，则返回登录页面
            if not check_password(password, user.password):
                return redirect('users:login')
            # 如果用户验证成，则修改session中的登录状态
            request.session['login_status'] = True
            # 2. cookie和session的应用
            # 2.1 向cookie中保存ticket参数
            ticket = get_random_ticket()
            out_time = datetime.now() + timedelta(days=1)
            res = HttpResponseRedirect(reverse('home:index'))
            res.set_cookie('ticket', ticket, expires=out_time)
            # 2.2 向user_ticket表中存ticket参数，判断如果存在则修改，如果不存在则创建
            user_ticket = UserTicket.objects.filter(user=user).first()
            if user_ticket:
                # 更新user_ticket表数据
                user_ticket.ticket = ticket
                user_ticket.out_time = out_time
                user_ticket.save()
            else:
                # 创建user_ticket表数据
                UserTicket.objects.create(user=user, ticket=ticket, out_time=out_time)
            return res
        else:
            # 如果表单验证不成功，则可以从form.errors中获取到验证失败的错误信息
            return render(request, 'web/login.html', {'form': form, 'data': data})


class Logout(View):

    def get(self, request, *args, **kwargs):
        # 设置session中用户的登录状态为false
        request.session['login_status'] = False
        # 注销跳转到首页
        res = redirect('/')
        # 删除cookie中的ticket参数
        res.delete_cookie('ticket')
        return res


class Register(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回注册页面
        return render(request, 'web/register.html')

    def post(self, request, *args, **kwargs):
        # 获取post请求中传递的参数
        data = request.POST
        # 使用表单验证，如果form表单验证成功，则is_valid()为True，反之为False
        form = UserRegisterForm(data)
        if form.is_valid():
            # 表单验证成功以后，可以通过form的cleaned_data方法获取参数值
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # 保存用户信息，并且对密码加密
            User.objects.create(username=username, password=make_password(password), email=email)
            # 验证表单成功，保存用户信息成功，则跳转到商城首页
            return HttpResponseRedirect(reverse('home:index'))
        else:
            # 如果表单验证不成功，则可以从form.errors中获取到验证失败的错误信息
            return render(request, 'web/register.html', {'form': form, 'data': data})


class IsLogin(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return JsonResponse({'code': 200, 'msg': '请求成功', 'username': user.username})


class UserCenterOrder(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'web/user_center_info.html')


class Address(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_addresses = UserAddress.objects.filter(user=user).order_by('-id').first()

        return render(request, 'web/user_center_site.html', {'user_addresses': user_addresses})

    def post(self, request, *args, **kwargs):
        form = UserAddressForm(request.POST)
        if form.is_valid():
            user = request.user
            address_info = form.cleaned_data
            UserAddress.objects.create(**address_info, user=user)
            return redirect('users:user_address')
        else:
            return render(request, 'web/user_center_site.html',{'form': form})
