#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : create_admin
# @Date     : 2018/11/05
# @Author   : Maliao
# @Link     : None


from test_script.django_env import *
from asset import models

# users = models.UserProfile.objects.filter(sex=1)
# for user in users:
#     user.sex = '男'
#     user.save()


# in_service_choice = (
#         ('在職', '在職'),
#         ('離職', '離職'),
#         ('停職', '停職'),
#         ('退休', '退休'),
#     )

status = ['未使用','使用中','遺失','報廢']
for i,v in enumerate(status):
    assets = models.Asset.objects.filter(status=i)
    for asset in assets:
        asset.status = v
        asset.save()



