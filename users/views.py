
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from users.forms import UserRegisterForm, UserLoginForm
from users.models import User, UserTicket
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

