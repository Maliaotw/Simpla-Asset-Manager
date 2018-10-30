# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-30 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_auto_20181020_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='status',
            field=models.IntegerField(choices=[(1, '未使用'), (2, '使用中'), (3, '遺失'), (4, '報廢')], default=1, verbose_name='狀態'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset',
            name='sn',
            field=models.CharField(max_length=255, verbose_name='資產編號'),
        ),
    ]