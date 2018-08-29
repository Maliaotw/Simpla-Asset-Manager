#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : linux_mem_1
# @Date     : 2018/8/29
# @Author   : Maliao
# @Link     : None

###### Memory Info of a Linux machine.
from __future__ import print_function
from collections import OrderedDict
import subprocess

def meminfo():

    f = open('/proc/meminfo')

    line = f.readline()
    mem = line.split(":")[1].strip().split(" ")[0]
    print(mem) # 4046488
    mb = int(1024 * 1024)
    ram_size = int(mem) / mb
    print(ram_size) # 3.8590316772460938


meminfo = meminfo()
# print('Total memory: {0}'.format(meminfo['MemTotal']))
# print('Free memory: {0}'.format(meminfo['MemFree']))


def meminfo2():
    mem = subprocess.getoutput("grep MemTotal /proc/meminfo | awk '{print $2 / 1024}'")
    return mem

ram_size = meminfo2()
print(ram_size)
