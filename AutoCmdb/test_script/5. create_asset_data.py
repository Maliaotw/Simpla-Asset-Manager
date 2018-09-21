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

    cate = Catagory.objects.all()
    dent = Department.objects.all()

    c = choice(cate)
    as_count = Asset.objects.filter(category=c).count() + 1
    num = "%03d" % as_count

    Asset.objects.create(sn=num,price=400,category=c,department=choice(dent))




