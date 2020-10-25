# Generated by Django 2.2.13 on 2020-10-25 07:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backManage', '0004_auto_20201025_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemvar',
            name='username',
            field=models.CharField(default='管理员', max_length=30, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='college',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 7, 23, 11, 46123, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 7, 23, 11, 47123, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='judge',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 7, 23, 11, 53124, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='member',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 7, 23, 11, 48123, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='systemvar',
            name='score_range',
            field=models.PositiveIntegerField(default=30, verbose_name='得分全距'),
        ),
        migrations.AlterField(
            model_name='systemvar',
            name='work_num',
            field=models.PositiveIntegerField(default=50, verbose_name='评委最多评审作品数'),
        ),
        migrations.AlterField(
            model_name='team',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 7, 23, 11, 49123, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='work',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 7, 23, 11, 52123, tzinfo=utc)),
        ),
    ]