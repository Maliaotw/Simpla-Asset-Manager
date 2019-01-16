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

        if user == asset_obj.manager:
            selected = "selected"
        else:
            selected = ""
        txt += '''<option %s value="%s">%s部(%s%s) </option>''' % (
            selected, user.id, user.name, user.dent.block_number, user.code)

    return mark_safe(txt)


@register.simple_tag
def get_pageer(data, search_field):
    # print(data)
    # print(data.number)  # 當前頁
    # print(data.paginator)  # paginator對象
    # print("num_pages",data.paginator.num_pages)  # 總頁數
    # print("count",data.paginator.count)
    # print(data.paginator.page_range)  # range(1, 15)

    # print('search_field',search_field)
    # print('data.has_previous()',data.has_previous())

    # 拼接搜尋字段
    search_str = ""
    if search_field:
        for k, v in search_field.items():
            search_str += '&%s=%s' % (k, v)
        # print(search_str)

    txt = ""

    part1 = 0
    part2 = 0

    # print("data.has_previous", data.has_previous())

    # 最前頁
    if data.has_previous():
        # <li><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
        # txt += '<a class="icon item" href="?page=1%s"><i class="left chevron icon"></i></a>' % search_str
        txt += '<li><a href="?page=1%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % search_str

    if data.paginator.num_pages > 10:

        # 當前頁 減五 大於0 那麼 當前頁 -5
        if data.number - 5 > 0:
            part1 = data.number - 5
        else:
            part1 = 1
            # 當前頁小於五 則 當前頁-減五加一
            part2 = abs(data.number - 5) + 1

        # 總頁數 - 當前頁 大於四 那麼 當前頁+4
        if data.paginator.num_pages - data.number > 5:
            part2 += data.number + 5
        else:
            # print("data.paginator.num_pages - part1", 10 - (data.paginator.num_pages - part1))
            part2 = data.paginator.num_pages+1
            part1 = part1 - (10 - (data.paginator.num_pages - part1))

        # print(part1, part2)

    else:
        part1 = 1
        part2 = data.paginator.num_pages + 1

    for page_number in range(part1, part2):

        if page_number == data.number:
            # <li class="page-item active"><a class="page-link" href="#">2 <span class="sr-only">(current)</span></a></li>
            # txt += '<a class="active item" href="?page=%s%s">%s</a>' % (page_number, search_str, page_number)
            txt += '<li class="page-item active"><a class="page-link" href="?page=%s%s">%s<span class="sr-only">(current)</span></a></li>' % (page_number, search_str, page_number)
        else:
            # <li class="page-item"><a class="page-link" href="#">1</a></li>
            # txt += '<a class="item" href="?page=%s%s">%s</a>' % (page_number, search_str, page_number)
            txt += '<li class="page-item"><a class="page-link" href="?page=%s%s"">%s</a></li>' % (
                page_number, search_str, page_number)

    # 最末頁
    if data.has_next():
        # <li><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
        # txt += '<a class="icon item" href="?page=%s%s"><i class="right chevron icon"></i></a>' % (data.paginator.num_pages, search_str)
        txt += '<li><a href="?page=%s%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>' % (data.paginator.num_pages, search_str)

    return mark_safe(txt)


@register.simple_tag
def get_category_column(category_obj):
    return models.Asset.objects.filter(category=category_obj).count()


@register.simple_tag
def verify_permissions(request):
    print('verify_permissions')
    print('test')
    # print(request)

    # 驗證用戶
    admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
    # print('admindent', admindent)

    if request.user.userprofile.dent in admindent:
        print('管理用戶')
        return True
    else:
        print('一般用戶')
        return False



@register.simple_tag
def verify_dent(request,code):
    '''

    :param request:
    :param code: dent_id
    :return:
    '''

    user = models.UserProfile.objects.get(user=request.user)

    if user.dent.code == code:
        return True
    else:
        return False




