

from .base import BasePlugin


class NicPlugin(BasePlugin):

    def windows(self):
        data = []
        for nic in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                item_data = {}
                item_data['macaddress'] = nic.MACAddress
                item_data['model'] = nic.Caption
                item_data['name'] = nic.Index
                if nic.IPAddress is not None:
                    item_data['ipaddress'] = nic.IPAddress[0]
                    item_data['netmask'] = nic.IPSubnet
                else:
                    item_data['ipaddress'] = ''
                    item_data['netmask'] = ''
                data.append(item_data)
        return data

    def linux(self):
        raw_data = self.exec_shell_cmd("ifconfig -a")

        raw_data = raw_data.split("\n")

        nic_dic = {}
        next_ip_line = False
        last_mac_addr = None
        for line in raw_data:
            if next_ip_line:
                # print last_mac_addr
                # print line #, last_mac_addr.strip()
                next_ip_line = False
                nic_name = last_mac_addr.split()[0]
                mac_addr = last_mac_addr.split("HWaddr")[1].strip()
                raw_ip_addr = line.split("inet addr:")
                raw_bcast = line.split("Bcast:")
                raw_netmask = line.split("Mask:")
                if len(raw_ip_addr) > 1:  # has addr
                    ip_addr = raw_ip_addr[1].split()[0]
                    network = raw_bcast[1].split()[0]
                    netmask = raw_netmask[1].split()[0]
                    # print(ip_addr,network,netmask)
                else:
                    ip_addr = None
                    network = None
                    netmask = None
                if mac_addr not in nic_dic:
                    nic_dic[mac_addr] = {'name': nic_name,
                                         'macaddress': mac_addr,
                                         'netmask': netmask,
                                         'network': network,
                                         'bonding': 0,
                                         'model': 'unknown',
                                         'ipaddress': ip_addr,
                                         }
                else:  # mac already exist , must be boding address
                    if '%s_bonding_addr' % (mac_addr) not in nic_dic:
                        random_mac_addr = '%s_bonding_addr' % (mac_addr)
                    else:
                        random_mac_addr = '%s_bonding_addr2' % (mac_addr)

                    nic_dic[random_mac_addr] = {'name': nic_name,
                                                'macaddress': random_mac_addr,
                                                'netmask': netmask,
                                                'network': network,
                                                'bonding': 1,
                                                'model': 'unknown',
                                                'ipaddress': ip_addr,
                                                }

            if "HWaddr" in line:
                # print line
                next_ip_line = True
                last_mac_addr = line

        nic_list = []
        for k, v in nic_dic.items():
            nic_list.append(v)

        return nic_list






