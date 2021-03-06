# Generated by Django 2.0.7 on 2018-08-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20180827_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('TRADE_FINISHED', '交易结束'), ('TRADE_CLOSE', '交易关闭'), ('WAIT_BUYER_PAY', '交易创建'), ('paying', '待支付'), ('TRADE_SUCCESS', '成功')], default='paying', max_length=20, verbose_name='交易状态'),
        ),
    ]
