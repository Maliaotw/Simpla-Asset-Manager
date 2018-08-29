#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : linux_disk_1
# @Date     : 2018/8/29
# @Author   : Maliao
# @Link     : None

import subprocess

def get_disk_info():
    disks = subprocess.getoutput("sudo /sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'")

    disks = disks.split("\n")

    print(disks)

    disk_list = []

    for index,disk in enumerate(disks):
        # print(disk)
        data = {}

        driver, disk_size = disk.split(",")[0].split(":")
        driver = driver.split(" ")[1]
        disk_size = disk_size.strip()

        data['slot'] = index
        # print(driver.split(" ")[0])
        data['disk_size'] = disk_size.strip().split(" ")[0]
        # print(disk_size.strip().split(" ")[0])


        detail = subprocess.getoutput("sudo hdparm -i %s | grep Model" % driver)
        # print(detail)

        for i in detail.split(','):
            k,v = i.split("=")
            data[k.strip()]=v.strip()

        data["sn"] = data['SerialNo']

        # print(data)
        disk_list.append(data)

    return data







    # 'sudo hdparm -i /dev/sda | grep Model'




print(get_disk_info())
