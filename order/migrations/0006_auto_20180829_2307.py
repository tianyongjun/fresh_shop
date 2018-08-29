# Generated by Django 2.0.7 on 2018-08-29 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20180828_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('paying', '待支付'), ('WAIT_BUYER_PAY', '交易创建'), ('TRADE_FINISHED', '交易结束'), ('TRADE_CLOSE', '交易关闭'), ('TRADE_SUCCESS', '成功')], default='paying', max_length=20, verbose_name='交易状态'),
        ),
    ]
