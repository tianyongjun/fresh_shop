# Generated by Django 2.0.7 on 2018-08-25 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='姓名'),
        ),
    ]
