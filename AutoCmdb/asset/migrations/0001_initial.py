# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-08 07:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='資產編號')),
                ('number', models.IntegerField(max_length=255, verbose_name='資產號碼')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='價格')),
                ('purchase_date', models.DateField(blank=True, null=True, verbose_name='購買日期')),
                ('status', models.CharField(choices=[('未使用', '未使用'), ('使用中', '使用中'), ('遺失', '遺失'), ('報廢', '報廢')], default='未使用', max_length=16, verbose_name='狀態')),
                ('latest_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='創建日期')),
            ],
            options={
                'verbose_name_plural': '資產信息表',
                'permissions': (('can_view_asset', 'Can view asset'),),
            },
        ),
        migrations.CreateModel(
            name='AssetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(1, '自動上傳'), (2, 'IT維護')], default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='創建日期')),
                ('asset_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset')),
            ],
            options={
                'verbose_name_plural': '資產紀錄表',
            },
        ),
        migrations.CreateModel(
            name='AssetRepair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='標題')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='內文')),
                ('status', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='創建日期')),
                ('finish_date', models.DateTimeField(blank=True, null=True, verbose_name='完成日期')),
                ('asset_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Asset', verbose_name='資產編號')),
            ],
            options={
                'verbose_name_plural': '資產維修表',
            },
        ),
        migrations.CreateModel(
            name='AssetRepairDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '資產維修詳細紀錄表',
            },
        ),
        migrations.CreateModel(
            name='AssetRepairImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name_plural': '資產紀錄圖片表',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名稱')),
                ('code', models.CharField(max_length=255, verbose_name='代號')),
            ],
            options={
                'verbose_name_plural': '類型',
                'permissions': (('can_view_category', 'Can view category'),),
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='部門名稱')),
                ('code', models.CharField(max_length=128, verbose_name='部門簡稱')),
                ('block_number', models.CharField(max_length=128, verbose_name='部門工/代號')),
                ('block_number_len', models.PositiveIntegerField(verbose_name='部門工/代號碼長度')),
            ],
            options={
                'verbose_name_plural': '部門',
                'permissions': (('can_view_department', 'Can view department'),),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '位置',
                'permissions': (('can_view_location', 'Can view location'),),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('code', models.CharField(blank=True, max_length=64, null=True, verbose_name='員工編號')),
                ('number', models.CharField(blank=True, max_length=64, null=True, verbose_name='員工號碼')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=16, verbose_name='性別')),
                ('in_service', models.CharField(choices=[('在職', '在職'), ('離職', '離職'), ('停職', '停職'), ('退休', '退休')], max_length=64, verbose_name='在職狀態')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日日期')),
                ('dent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.Department', verbose_name='部門')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名')),
            ],
            options={
                'verbose_name_plural': '用戶',
                'permissions': (('can_view_userprofile', 'Can view UserProfile'), ('can_change_userprofile', 'Can change UserProfile')),
            },
        ),
        migrations.AddField(
            model_name='department',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.UserProfile', verbose_name='部門負責人'),
        ),
        migrations.AddField(
            model_name='assetrepairdetail',
            name='photo',
            field=models.ManyToManyField(blank=True, null=True, to='asset.AssetRepairImage'),
        ),
        migrations.AddField(
            model_name='assetrepairdetail',
            name='repair',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.AssetRepair'),
        ),
        migrations.AddField(
            model_name='assetrepairdetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.UserProfile'),
        ),
        migrations.AddField(
            model_name='assetrepair',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='asset.UserProfile', verbose_name='創建者'),
        ),
        migrations.AddField(
            model_name='assetrepair',
            name='photo',
            field=models.ManyToManyField(blank=True, null=True, to='asset.AssetRepairImage'),
        ),
        migrations.AddField(
            model_name='assetrepair',
            name='repairer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='asset.UserProfile', verbose_name='維修者'),
        ),
        migrations.AddField(
            model_name='assetrecord',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='asset.UserProfile', verbose_name='創建者'),
        ),
        migrations.AddField(
            model_name='asset',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Category', verbose_name='類型'),
        ),
        migrations.AddField(
            model_name='asset',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.Department', verbose_name='部門'),
        ),
        migrations.AddField(
            model_name='asset',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.UserProfile', verbose_name='負責人'),
        ),
    ]
