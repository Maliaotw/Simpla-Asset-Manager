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

User.objects.all().delete()
UserProfile.objects.all().delete()

dent_obj = Department.objects.get(code="OM")

# 部門人數
user_count = UserProfile.objects.filter(code="OM").count() + 1

# 部門編號
block_number = dent_obj.block_number

# 部門長度

block_number_len = dent_obj.block_number_len

num_format = "%0{}d".format(block_number_len - len(block_number))  # block_numer_len

num = num_format % (user_count)  # block_numer
code="%s%s" % (block_number,num)
print(num)
print(code)


user = User()
user.username = "Tony"
user.set_password("12345678")
user.is_staff = True
user.is_superuser = True
user.save()
UserProfile.objects.create(
    user=user,name="托尼",sex=1,dent=dent_obj,number=num,code=code
)


