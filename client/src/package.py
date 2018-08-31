#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : package
# @Date     : 2018/8/30
# @Author   : Maliao
# @Link     : None

from .plugins.disk import DiskPlugin
from .plugins.mem import MemPlugin
from .plugins.nic import NicPlugin


def pack():
    obj1 = DiskPlugin()
    disk_info = obj1.execute()
    obj2 = MemPlugin()
    mem_info = obj2.execute()
    obj3 = NicPlugin()
    nic_info = obj3.execute()

    response = {
        'disk': disk_info,
        'mem': mem_info,
        'nic':nic_info
    }

    return response
