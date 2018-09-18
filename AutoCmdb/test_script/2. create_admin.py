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

dent_OM = Department.objects.get(code="OM")
as_count = UserProfile.objects.filter(dent=dent_OM).count() + 1
num = "%02d" % as_count


user = User()
user.username = "Tony"
user.set_password("12345678")
user.is_staff = True
user.is_superuser = True
user.save()
UserProfile.objects.create(user=user,name="托尼",sex=1,dent=dent_OM,code=num)





