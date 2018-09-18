#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : create_admin
# @Date     : 2018/9/13
# @Author   : Maliao
# @Link     : None

from test_script.django_env import *
from django.contrib.auth.models import User
from host.models import *
from asset.models import *
from random import choice

Department.objects.all().delete()

'''
name = models.CharField(max_length=255,verbose_name="部門名稱")
code = models.CharField(max_length=128,verbose_name='部門簡稱')
block_number = models.CharField(max_length=128,verbose_name='部門工/代號')
block_number_len = models.PositiveIntegerField(verbose_name='部門工/代號碼長度')
user = models.ForeignKey('UserProfile',verbose_name='部門負責人',blank=True,null=True)

'''

# 部門
department = [
    {'code': 'HR', 'name': '人資','block_number':'1','block_number_len':3},
    {'code': 'IT', 'name': '資訊','block_number':'2','block_number_len':3},
    {'code': 'RD', 'name': '研發','block_number':'3','block_number_len':3},
    {'code': 'PR', 'name': '公關','block_number':'4','block_number_len':3},
    {'code': 'CS', 'name': '客服','block_number':'5','block_number_len':3},
    {'code': 'OM', 'name': '運營','block_number':'0','block_number_len':3},

]

for d in department:
    Department.objects.create(**d)