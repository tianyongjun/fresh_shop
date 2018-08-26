from django.db import models

from goods.models import Goods


class Banner(models.Model):
    goods = models.ForeignKey(Goods, related_name='banner', verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner/images', verbose_name='轮播图')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_banner'
