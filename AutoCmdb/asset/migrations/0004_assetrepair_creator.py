# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-01-03 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_remove_assetrepair_repairer'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetrepair',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.UserProfile', verbose_name='創建者'),
        ),
    ]