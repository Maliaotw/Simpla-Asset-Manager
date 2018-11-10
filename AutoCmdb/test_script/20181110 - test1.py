#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : create_admin
# @Date     : 2018/11/05
# @Author   : Maliao
# @Link     : None


from test_script.django_env import *
# from asset import models
from host import models

# users = models.UserProfile.objects.filter(sex=1)
# for user in users:
#     user.sex = '男'
#     user.save()



host_type_ids = ['工作站','值班電腦','培訓電腦','備用電腦','汰換機','測試機']
for i,v in enumerate(host_type_ids):
    hosts = models.Host.objects.filter(host_type_id=i)
    for host in hosts:
        host.host_type_id = v
        host.save()



