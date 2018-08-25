
from django import forms
from django.contrib.auth.hashers import check_password

from users.models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=5,
                               error_messages={'required': '请输入5-20个字符的用户名',
                                               'max_length': '用户名不能超过20个字符',
                                               'min_length': '用户名不能少于5个字符'}
                               )
    password = forms.CharField(required=True, max_length=20, min_length=8,
                               error_messages={'required': '密码最少8位，最长20位',
                                               'max_length': '最长20位',
                                               'min_length': '密码最少8位'}
                               )
    password2 = forms.CharField(required=True, error_messages={'required':'确认密码必填'})
    email = forms.CharField(required=True, error_messages={'required':'邮箱必填'})
    allow = forms.BooleanField(required=True, error_messages={'required':'请勾选同意'})

    def clean(self):
        # 获取用户名和密码
        username = self.cleaned_data.get('username')
        # 验证用户名是否存在
        user = User.objects.filter(username=username).first()
        if user:
            # 如果用户名存在，则提示用户名已存在
            raise forms.ValidationError({'username': '用户名已存在'})
        return self.cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True,
                               error_messages={'required': '用户名必填'})
    password = forms.CharField(required=True,
                               error_messages={'required': '密码必填'})


    def clean(self):
        # 获取用户名和密码
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # 验证用户名是否存在
        user = User.objects.filter(username=username).first()
        if not user:
            # 如果用户名不存在，则提示先注册
            raise forms.ValidationError({'username':'用户名不存在，请先注册'})

        # 验证用户名是否正确
        if not check_password(password, user.password):
            raise forms.ValidationError({'password':'密码错误'})

        return self.cleaned_data
