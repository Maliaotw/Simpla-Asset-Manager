#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : asset_tags.py
# @Date     : 2018/9/20
# @Author   : Maliao
# @Link     : None

from django import template
from django.utils.safestring import mark_safe
from asset import models
from django.contrib.auth.models import User
import datetime

register = template.Library()


@register.simple_tag
def get_dent_user_column0(asset_obj, request):


    dent_obj = models.Department.objects.all()
    users = models.UserProfile.objects.filter(dent=dent_obj)


    txt = '''
    <td name="department">
                        <span class="form-control-static">
                           %s
                        </span>

                        <select class="form-control" onchange="get_dent_user(this)" style="display: none">
    ''' % (asset_obj.department)


    for dent in dent_obj:
        if asset_obj.department == dent:
            selected = 'selected'
        else:
            selected = ''

        txt += '''<option %s value="%s">%s部%s</option>''' % (selected, dent.id, dent.name, dent.code)

    txt += '''
    </select></td>
    '''


    txt += '''
    <td name="manager">
        <span class="form-control-static">
             %s
        </span>

        <select id='user_put' class="form-control" style="display: none">
        <option value="">------</option>
        ''' % asset_obj.manager




    txt +='''</select></td>'''



    return mark_safe(txt)


@register.simple_tag
def get_dent_user_column(asset_obj, request):

    dent_id = asset_obj.department.id
    dent_obj = models.Department.objects.get(id=dent_id)
    users_obj = models.Department.objects.filter(dent=dent_obj)

    txt = ""
    for user in users_obj:

        if user == asset_obj.manager :
            selected = "selected"
        else:
            selected = ""
        txt += '''<option %s value="%s">%s部(%s) </option>''' % (selected,asset_obj.id,asset_obj.name,asset_obj.code)

    return mark_safe(txt)





