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

user = User()
user.username = "maliao"
user.set_password("12345678")
user.is_staff = True
user.is_superuser = True
user.save()
UserProfile.objects.create(user=user,name="馬里奧",code=999)





