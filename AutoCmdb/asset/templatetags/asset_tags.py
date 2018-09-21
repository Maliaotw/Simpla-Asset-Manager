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
def get_dent_user_column(asset_obj, request):

    dent_obj = asset_obj.department
    users_obj = models.UserProfile.objects.filter(dent=dent_obj)

    txt = ""
    for user in users_obj:

        if user == asset_obj.manager :
            selected = "selected"
        else:
            selected = ""
        txt += '''<option %s value="%s">%s部(%s%s) </option>''' % (selected,user.id,user.name,user.dent.block_number,user.code)

    return mark_safe(txt)





