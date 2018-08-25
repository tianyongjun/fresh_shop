from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回首页
        return render(request, 'web/index.html')
