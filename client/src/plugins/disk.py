

from .base import BasePlugin



class DiskPlugin(BasePlugin):

    def windows(self):
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():
            item_data = {}
            iface_choices = ["SAS", "SCSI", "SATA", "SSD"]
            for iface in iface_choices:
                if iface in disk.Model:
                    item_data['iface_type'] = iface
                    break
            else:
                item_data['iface_type'] = 'unknown'
            item_data['slot'] = disk.Index
            item_data['sn'] = disk.SerialNumber.strip()
            item_data['model'] = disk.Model
            item_data['manufacturer'] = disk.Manufacturer
            item_data['capacity'] = int(disk.Size) / (1024 * 1024 * 1024)
            data.append(item_data)
        return data

    def linux(self):
        disks = self.exec_shell_cmd("sudo /sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'")
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

            detail = self.exec_shell_cmd("sudo hdparm -i %s | grep Model" % driver)
            # print(detail)

            for i in detail.split(','):
                k, v = i.split("=")
                data[k.strip()] = v.strip()

            data["sn"] = data['SerialNo']

            # print(data)
            disk_list.append(data)

        # print(disk_list)
        return disk_list








