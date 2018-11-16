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


# User.objects.all().delete()
# UserProfile.objects.all().delete()


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

# 讀取檔案

f = open('users.txt', 'r', encoding='utf-8')

ret = []

ret_user = []

for i in f:

    userline = i.split(' ')
    userline = list(filter(lambda x: x, userline))
    username = userline[0].strip()
    name = userline[1].strip()
    sex = userline[2].strip()
    data = {
        'username': username,
        'name': name,
        'sex': sex
    }
    if username in ret_user:
        pass
    else:
        ret.append(data)
        ret_user.append(username)




# --- 創建用戶


for u in ret:
    # dent
    dents = Department.objects.exclude(code='OM')
    dent = choice(dents)
    as_count = UserProfile.objects.filter(dent=dent).count() + 1

    # 部門編號
    block_number = dent.block_number
    # 部門長度
    block_number_len = dent.block_number_len
    num_format = "%0{}d".format(block_number_len - len(block_number))  # block_numer_len
    num = num_format % (as_count)  # block_numer
    code = "%s%s" % (block_number, num)


    user = User()
    user.username = u['username']
    user.set_password('12345678')
    user.is_staff = False
    user.save()
    UserProfile.objects.create(user=user, name=u['name'], sex=u['sex'],code=code,dent=dent,number=num)



