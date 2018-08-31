

from .base import BasePlugin
import subprocess


class DiskPlugin(BasePlugin):

    def windows(self):
        pass

    def linux(self):
        disks = subprocess.getoutput("sudo /sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'")
        # print(disks)
        disks = disks.split("\n")
        disk_list = []

        for index, disk in enumerate(disks):
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
                k, v = i.split("=")
                data[k.strip()] = v.strip()

            data["sn"] = data['SerialNo']

            # print(data)
            disk_list.append(data)

        # print(disk_list)
        return disk_list








