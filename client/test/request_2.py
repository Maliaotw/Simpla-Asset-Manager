#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : request_1
# @Date     : 2018/9/1
# @Author   : Maliao
# @Link     : None


import requests
import hashlib
import time


data = {
    'cpu': {'cpu_count': 1, 'cpu_core_count': 2, 'cpu_model': 'Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz'},
    'nic': [
        {'model': '[00000001] VPN Client Adapter - VPN', 'name': 1, 'netmask': '', 'macaddress': '00:AC:39:5C:AA:19',
         'ipaddress': ''},
        {'model': '[00000002] TAP-Windows Adapter V9', 'name': 2, 'netmask': '', 'macaddress': '00:FF:AE:09:80:29',
         'ipaddress': ''},
        {'model': '[00000005] Realtek PCIe GBE Family Controller', 'name': 5, 'netmask': ('255.255.255.0', '64'),
         'macaddress': '54:E1:AD:2A:C7:98', 'ipaddress': '192.168.8.15'},
        {'model': '[00000006] Qualcomm Atheros QCA61x4A Wireless Network Adapter', 'name': 6,
         'netmask': ('255.255.255.0', '64'), 'macaddress': 'F8:28:19:C0:99:23', 'ipaddress': '192.168.80.31'},
        {'model': '[00000007] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 7, 'netmask': '',
         'macaddress': 'FA:28:19:C0:99:23', 'ipaddress': ''},
        {'model': '[00000008] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 8, 'netmask': '',
         'macaddress': '0A:28:19:C0:99:23', 'ipaddress': ''},
        {'model': '[00000010] Bluetooth Device (Personal Area Network)', 'name': 10, 'netmask': '',
         'macaddress': 'F8:28:19:C0:99:24', 'ipaddress': ''},
        {'model': '[00000016] WAN Miniport (IP)', 'name': 16, 'netmask': '', 'macaddress': '34:98:20:52:41:53',
         'ipaddress': ''},
        {'model': '[00000017] WAN Miniport (IPv6)', 'name': 17, 'netmask': '', 'macaddress': '40:DB:20:52:41:53',
         'ipaddress': ''},
        {'model': '[00000018] WAN Miniport (Network Monitor)', 'name': 18, 'netmask': '',
         'macaddress': '4E:96:20:52:41:53',
         'ipaddress': ''}], 'mem': None,
    'basic': {'model': '20H5A036TW', 'wake_up_type': 6, 'sn': '00325-96159-04707-AAOEM', 'manufactory': 'LENOVO',
              'os_distribution': 'Microsoft', 'os_type': ('Windows',), 'os_release': ('10 64bit  10.0.17134 ',)},
    'disk': [{'manufactory': '(标准磁盘驱动器)', 'capacity': 238.4679079055786, 'slot': 1, 'sn': '2H0620041910',
              'model': 'ADATA SU800NS38', 'iface_type': 'unknown'},
             {'manufactory': '(标准磁盘驱动器)', 'capacity': 465.7593083381653, 'slot': 0, 'sn': '           544TC4OZT',
              'model': 'SanDisk SD8SB8U256G1122', 'iface_type': 'unknown'}]}


import json

current_time = time.time()
app_id = "mdfmsijfiosdjoidfjdf"
app_id_time = "%s|%s" % (app_id,current_time)


m = hashlib.md5()
m.update(bytes(app_id_time, encoding='utf-8'))
authkey = m.hexdigest()
# print(authkey)

authkey_time = "%s|%s" % (authkey,current_time)

r = requests.post(
    url="http://127.0.0.1:8000/api/asset",
    json=json.dumps(data),
    headers={'authkey': "65cf888a0857c12d2d01c42ba9897560|1536138465.9408777"}
)

print(authkey_time)
print(r.text)
