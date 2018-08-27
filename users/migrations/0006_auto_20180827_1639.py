# Generated by Django 2.0.7 on 2018-08-27 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_useraddress_userfav_userleavingmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userleavingmessage',
            name='message_type',
            field=models.IntegerField(choices=[(2, '投诉'), (1, '留言'), (4, '售后'), (3, '咨询')], default=1, help_text='留言类型: 1(留言),2(投诉),3(咨询),4(售后)', verbose_name='留言类型'),
        ),
    ]
