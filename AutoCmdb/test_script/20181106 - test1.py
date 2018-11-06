#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : create_admin
# @Date     : 2018/11/06
# @Author   : Maliao
# @Link     : None


verbose_name = ['用户名', '姓名', '員工編號', '性別', '部門', '在職狀態', '生日日期']
field_name = ['username', 'name', 'code', 'sex', 'dent', 'in_service', 'birthday']


data = { k : {'name':name} for k,name in zip(field_name,verbose_name)}
print(data)



