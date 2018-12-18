

from .base import BasePlugin


class MemPlugin(BasePlugin):

    def windows(self):
        data = []
        ram_collections = self.wmi_service_connector.ExecQuery("Select * from Win32_PhysicalMemory")
        for item in ram_collections:
            mb = int(1024 * 1024)
            ram_size = int(item.Capacity) / mb
            item_data = {
                "slot": item.DeviceLocator.strip(),
                "capacity": ram_size,
                "model": item.Caption,
                "manufacturer": item.Manufacturer,
                "sn": item.SerialNumber,
            }
            data.append(item_data)
        return data

    def linux(self):
        # raw_data = subprocess.check_output(["sudo", "dmidecode" ,"-t", "17"])
        raw_data = self.exec_shell_cmd("sudo dmidecode -t 17")
        raw_list = raw_data.split("\n")
        raw_ram_list = []
        item_list = []
        for line in raw_list:

            if line.startswith("Memory Device"):
                raw_ram_list.append(item_list)
                item_list = []
            else:
                item_list.append(line.strip())

        ram_list = []
        for item in raw_ram_list:
            item_ram_size = 0
            ram_item_to_dic = {}
            for i in item:
                # print i
                data = i.split(":")
                if len(data) == 2:
                    key, v = data

                    if key == 'Size':
                        # print key ,v
                        if v.strip() != "No Module Installed":
                            ram_item_to_dic['capacity'] = v.split()[0].strip()  # e.g split "1024 MB"
                            item_ram_size = int(v.split()[0])
                            # print item_ram_size
                        else:
                            ram_item_to_dic['capacity'] = 0

                    if key == 'Type':
                        ram_item_to_dic['model'] = v.strip()
                    if key == 'Manufacturer':
                        ram_item_to_dic['manufacturer'] = v.strip()
                    if key == 'Serial Number':
                        ram_item_to_dic['sn'] = v.strip()
                    if key == 'Asset Tag':
                        ram_item_to_dic['asset_tag'] = v.strip()
                    if key == 'Locator':
                        ram_item_to_dic['slot'] = v.strip()

                    # if i.startswith("")
            if item_ram_size == 0:  # empty slot , need to report this
                pass
            else:
                ram_list.append(ram_item_to_dic)

        # get total size(mb) of ram as well
        # raw_total_size = subprocess.check_output(" cat /proc/meminfo|grep MemTotal ",shell=True).split(":")
        raw_total_size = self.exec_shell_cmd("cat /proc/meminfo|grep MemTotal ").split(":")
        ram_data = {'ram': ram_list}
        if len(raw_total_size) == 2:  # correct

            total_mb_size = int(raw_total_size[1].split()[0]) / 1024
            ram_data['ram_size'] = total_mb_size
            # print(ram_data)

        print(ram_data)
        return ram_list




