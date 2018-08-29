"""fresh_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from django.contrib.staticfiles.urls import static
from django.views.static import serve

from fresh_shop import settings
from home import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户地址
    path('users/', include(('users.urls', 'users'), namespace='users')),
    # 商品地址
    path('goods/', include(('goods.urls', 'goods'), namespace='goods')),
    # 生鲜前台地址
    path('home/', include(('home.urls', 'home'), namespace='home')),
    # 访问生鲜首页地址
    re_path(r'^$', views.Index.as_view()),

    # 配置media路径
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# 配置media访问路径
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


