# Generated by Django 2.0.7 on 2018-08-28 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180827_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userleavingmessage',
            name='message_type',
            field=models.IntegerField(choices=[(3, '咨询'), (4, '售后'), (1, '留言'), (2, '投诉')], default=1, help_text='留言类型: 1(留言),2(投诉),3(咨询),4(售后)', verbose_name='留言类型'),
        ),
    ]
