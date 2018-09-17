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

'''
user = models.OneToOneField(User)
name = models.CharField(max_length=64, verbose_name="暱稱")
code = models.IntegerField(verbose_name='員工編號',blank=True,null=True)

sex_choice = (
    (1, '男'),
    (2, '女'),
)

sex = models.IntegerField(choices=sex_choice)
dent = models.ForeignKey('Department',verbose_name='部門',blank=True,null=True)
'''

# 創建用戶

# http://www.resgain.net/english_names.html

users = [
    {'username':'Aabbye','name':'',}
]

users = ["Aaron", "Abbas", "Christine", "Gardner"]
passwd = "12345678"

for i, name in enumerate(users):
    user = User()
    user.username = name
    user.set_password(passwd)
    user.is_staff = True
    user.save()
    UserProfile.objects.create(user=user, name=name, code=i)




