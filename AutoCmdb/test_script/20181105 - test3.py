#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : create_admin
# @Date     : 2018/11/05
# @Author   : Maliao
# @Link     : None


from test_script.django_env import *
from asset import models

sex_list = ['男','女']

# u = models.UserProfile.objects.filter(sex='2')
# print(u)

for i,v in enumerate(sex_list):
    print(int(i)+1)
    sex = int(i)+1
    users = models.UserProfile.objects.filter(sex=sex)
    for user in users:
        user.sex = v
        user.save()


