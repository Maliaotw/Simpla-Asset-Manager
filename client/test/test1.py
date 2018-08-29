#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : test1
# @Date     : 2018/8/29
# @Author   : Maliao
# @Link     : None


import os
import platform
import wmi

# ---- Windows 採集系統 信息 ----


wmi_obj = wmi.WMI()



# 抓系統

os = platform.system()
print(os) # Windows

platform.release() # '10'


# 硬盤

# CPU

def get_cpu_info():
    data = {}
    cpu_lists = wmi_obj.Win32_Processor()
    cpu_core_count = 0

    for cpu in cpu_lists:
        cpu_core_count += cpu.NumberOfCores
        cpu_model = cpu.Name
    data["cpu_count"] = len(cpu_lists)
    data["cpu_model"] = cpu_model
    data["cpu_core_count"] = cpu_core_count
    return data


print(get_cpu_info())


# 主板


# 網卡






