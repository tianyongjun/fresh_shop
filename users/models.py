from django.db import models

from goods.models import Goods


class User(models.Model):
    """
     用户表
    """
    username = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="姓名")
    password = models.CharField(max_length=255, verbose_name="密码")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    GENDER = (
        ("male", u"男"),
        ("female", "女")
    )
    gender = models.CharField(max_length=6, choices=GENDER, default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        db_table = 'f_user'


class UserTicket(models.Model):
    """
    用户和登录验证ticket参数对应表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.CharField(max_length=40)
    out_time = models.DateTimeField()

    class Meta:
        db_table = 'f_user_ticket'


class UserAddress(models.Model):
    """
    收货地址表
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default='', verbose_name='省份')
    city = models.CharField(max_length=100, default='', verbose_name='城市')
    district = models.CharField(max_length=100, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='电话')
    signer_postcode = models.CharField(max_length=11, default='', verbose_name='邮编')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_user_address'


class UserLeavingMessage(models.Model):
    """
    用户留言表
    """
    MESSAGE_CHOICE = {
        (1, '留言'),
        (2, '投诉'),
        (3, '咨询'),
        (4, '售后')
    }
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICE, verbose_name='留言类型',
                                       help_text='留言类型: 1(留言),2(投诉),3(咨询),4(售后)')
    subject = models.CharField(max_length=100, default='', verbose_name='主题')
    message = models.TextField(default='', verbose_name='留言内容')
    file = models.FileField(upload_to='message/images/', verbose_name='上传的文件')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_user_leaving_message'


class UserFav(models.Model):
    """
    用户收藏表
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_user_fav'