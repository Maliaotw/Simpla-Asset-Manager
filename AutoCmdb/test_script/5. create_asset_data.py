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

Asset.objects.all().delete()

for i in range(200):

    cate_obj = Category.objects.all()
    dent_obj = Department.objects.all()

    cate = choice(cate_obj)
    as_count = Asset.objects.filter(category=cate).count() + 1
    num = "%03d" % as_count
    name = "%s-%s" % (cate.code,num)
    print(num)
    print(name)

    Asset.objects.create(number=num,name=name,price=400,category=cate,department=choice(dent_obj),status='使用中')




