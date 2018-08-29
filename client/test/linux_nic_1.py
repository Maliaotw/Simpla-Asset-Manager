#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : linux_nic_1
# @Date     : 2018/8/29
# @Author   : Maliao
# @Link     : None

import subprocess

def get_nic_info():
    """
    获取网卡信息
    :return:
    """
    raw_data = subprocess.Popen("ifconfig -a", stdout=subprocess.PIPE, shell=True)

    raw_data = raw_data.stdout.read().decode().split("\n")

    nic_dic = dict()
    next_ip_line = False
    last_mac_addr = None

    for line in raw_data:
        if next_ip_line:
            next_ip_line = False
            nic_name = last_mac_addr.split()[0]
            mac_addr = last_mac_addr.split("HWaddr")[1].strip()
            raw_ip_addr = line.split("inet addr:")
            raw_bcast = line.split("Bcast:")
            raw_netmask = line.split("Mask:")
            if len(raw_ip_addr) > 1:
                ip_addr = raw_ip_addr[1].split()[0]
                network = raw_bcast[1].split()[0]
                netmask = raw_netmask[1].split()[0]
            else:
                ip_addr = None
                network = None
                netmask = None
            if mac_addr not in nic_dic:
                nic_dic[mac_addr] = {'name': nic_name,
                                     'mac': mac_addr,
                                     'net_mask': netmask,
                                     'network': network,
                                     'bonding': 0,
                                     'model': 'unknown',
                                     'ip_address': ip_addr,
                                     }
            else:
                if '%s_bonding_addr' % (mac_addr,) not in nic_dic:
                    random_mac_addr = '%s_bonding_addr' % (mac_addr,)
                else:
                    random_mac_addr = '%s_bonding_addr2' % (mac_addr,)

                nic_dic[random_mac_addr] = {'name': nic_name,
                                            'mac': random_mac_addr,
                                            'net_mask': netmask,
                                            'network': network,
                                            'bonding': 1,
                                            'model': 'unknown',
                                            'ip_address': ip_addr,
                                            }

        if "HWaddr" in line:
            next_ip_line = True
            last_mac_addr = line
    nic_list = []
    for k, v in nic_dic.items():
        nic_list.append(v)

    return {'nic': nic_list}

print(get_nic_info())
