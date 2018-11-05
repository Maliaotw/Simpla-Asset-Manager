#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : create_admin
# @Date     : 2018/11/05
# @Author   : Maliao
# @Link     : None


from test_script.django_env import *
from asset import models
from asset import forms
import datetime

data = {
    'username': 'maliao110500',
    'name': '馬里奧',
    'code': '149',
    'sex': '男',
    'dent': '人資',
    'in_service': '在職',
    'birthday': '2018/11/05',
    'is_staff': '22'

}

data['dent'] = models.Department.objects.filter(name=data['dent'])
data['birthday'] = datetime.datetime.strptime(data['birthday'], '%Y/%m/%d')


is_staff_coice = {'是':True,'否':False}
if data['is_staff'] in list(is_staff_coice.keys()):
    data['is_staff'] = is_staff_coice[data['is_staff']]



forms_obj = forms.User_Add_Form(data=data)
print(forms_obj.errors)
for e in forms_obj.errors:
    print(e)
