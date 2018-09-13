#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : test_data
# @Date     : 2018/9/13
# @Author   : Maliao
# @Link     : None


from test_script.django_env import *
from django.contrib.auth.models import User
from host.models import *
from asset.models import *

Catagory.objects.all().delete()
UserProfile.objects.all().delete()
User.objects.all().delete()
Department.objects.all().delete()
Host.objects.all().delete()
Location.objects.all().delete()

# 創建分類
cate_pc = Catagory.objects.create(name="電腦", code='PC')
cate_m = Catagory.objects.create(name="滑鼠", code='M')
cate_p = Catagory.objects.create(name="變壓器", code='P')
cate_a = Catagory.objects.create(name='延長線', code='A')

# 創建用戶
users = ["Aaron", "Abbas", "Christine", "Gardner"]
passwd = "12345678"

for i, name in enumerate(users):
    user = User()
    user.username = name
    user.set_password(passwd)
    user.is_staff = True
    user.save()
    UserProfile.objects.create(user=user, name=name, code=i)

# 部門
department = [
    {'code': 'HR', 'name': '人資'},
    {'code': 'IT', 'name': '資訊'},
    {'code': 'RD', 'name': '研發'},
    {'code': 'PR', 'name': '公關'},
    {'code': 'CS', 'name': '客服'},

]

for d in department:
    Department.objects.create(**d)

# 位置

location = ["辦公室", "機房"]
for l in location:
    Location.objects.create(name=l)

# PC

pcs = [
    {
        'cpu':
            {'cpu_count': 1, 'cpu_core_count': 2, 'cpu_model': 'Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz'},

        'basic':
            {'wake_up_type': 6, 'os_distribution': 'Microsoft', 'os_release': ('10 64bit  10.0.17134 ',),
             'sn': '09805-99999-01147-SDDED', 'model': '16LS98FATW', 'manufactory': 'LENOVO', 'os_type': ('Windows',)},

        "mem":
            [
                {'manufacturer': 'Samsung', 'sn': '999B51D9', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelA-DIMM0'},
                {'manufacturer': 'Samsung', 'sn': '4844855A', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelB-DIMM0'}
            ],
        'disk':
            [
                { 'capacity': 238.4679079055786, 'sn': '2H8488141910',
                 'model': 'ADATA SU800NS38', 'manufacturer': '(标准磁盘驱动器)', 'slot': 1},
                { 'capacity': 465.7593083381653, 'sn': '5954TO10ZT',
                 'model': 'SanDisk SD8SB8U256G1122', 'manufacturer': '(标准磁盘驱动器)', 'slot': 0}
            ],
        'nic':
            [
                {'ipaddress': '', 'macaddress': '00:AC:39:5C:AA:19', 'model': '[00000001] VPN Client Adapter - VPN',
                 'name': 1, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '00:FF:AE:09:80:29', 'model': '[00000002] TAP-Windows Adapter V9',
                 'name': 2, 'netmask': ''},
                {'ipaddress': '192.168.8.15', 'macaddress': '48:E9:EF:9F:D7:A8',
                 'model': '[00000005] Realtek PCIe GBE Family Controller', 'name': 5,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '192.168.80.55', 'macaddress': 'A6:28:20:0D:66:23',
                 'model': '[00000006] Qualcomm Atheros QCA61x4A Wireless Network Adapter', 'name': 6,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '', 'macaddress': 'FA:28:19:C0:99:23',
                 'model': '[00000007] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 7, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '0A:28:19:C0:99:23',
                 'model': '[00000008] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 8, 'netmask': ''},
                {'ipaddress': '', 'macaddress': 'F8:28:19:C0:99:24',
                 'model': '[00000010] Bluetooth Device (Personal Area Network)', 'name': 10, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '34:98:20:52:41:53', 'model': '[00000016] WAN Miniport (IP)',
                 'name': 16, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '40:DB:20:52:41:53', 'model': '[00000017] WAN Miniport (IPv6)',
                 'name': 17, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '4E:96:20:52:41:53',
                 'model': '[00000018] WAN Miniport (Network Monitor)', 'name': 18, 'netmask': ''}
            ],
    },

    {
        'cpu':
            {'cpu_count': 1, 'cpu_core_count': 2, 'cpu_model': 'Intel(R) Core(TM) i5-6200U CPU @ 2.50GHz'},

        'basic':
            {'wake_up_type': 6, 'os_distribution': 'Microsoft', 'os_release': ('10 64bit  10.0.17134 ',),
             'sn': '10185-99999-01147-SDDEB', 'model': '16LS98FATW', 'manufactory': 'LENOVO', 'os_type': ('Windows',)},

        "mem":
            [
                {'manufacturer': 'Samsung', 'sn': '888B51DB', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelA-DIMM0'},
                {'manufacturer': 'Samsung', 'sn': '4844855B', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelB-DIMM0'}
            ],
        'disk':
            [
                { 'capacity': 238.4679079055786, 'sn': '2H848814191B',
                 'model': 'ADATA SU800NS38', 'manufacturer': '(标准磁盘驱动器)', 'slot': 1},
                { 'capacity': 465.7593083381653, 'sn': '5954TO10ZB',
                 'model': 'SanDisk SD8SB8U256G', 'manufacturer': '(标准磁盘驱动器)', 'slot': 0}
            ],
        'nic':
            [
                {'ipaddress': '', 'macaddress': '00:AC:39:5C:AA:19', 'model': '[00000001] VPN Client Adapter - VPN',
                 'name': 1, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '00:FF:AE:09:80:29', 'model': '[00000002] TAP-Windows Adapter V9',
                 'name': 2, 'netmask': ''},
                {'ipaddress': '192.168.8.15', 'macaddress': '48:E9:EF:9F:D7:AB',
                 'model': '[00000005] Realtek PCIe GBE Family Controller', 'name': 5,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '192.168.80.55', 'macaddress': 'A6:28:20:0D:66:2B',
                 'model': '[00000006] Qualcomm Atheros QCA61x4A Wireless Network Adapter', 'name': 6,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '', 'macaddress': 'FA:28:19:C0:99:23',
                 'model': '[00000007] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 7, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '0A:28:19:C0:99:23',
                 'model': '[00000008] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 8, 'netmask': ''},
                {'ipaddress': '', 'macaddress': 'F8:28:19:C0:99:24',
                 'model': '[00000010] Bluetooth Device (Personal Area Network)', 'name': 10, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '34:98:20:52:41:53', 'model': '[00000016] WAN Miniport (IP)',
                 'name': 16, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '40:DB:20:52:41:53', 'model': '[00000017] WAN Miniport (IPv6)',
                 'name': 17, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '4E:96:20:52:41:53',
                 'model': '[00000018] WAN Miniport (Network Monitor)', 'name': 18, 'netmask': ''}
            ],
    },

    {
        'cpu':
            {'cpu_count': 1, 'cpu_core_count': 2, 'cpu_model': 'Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz'},

        'basic':
            {'wake_up_type': 6, 'os_distribution': 'Microsoft', 'os_release': ('10 64bit  10.0.17134 ',),
             'sn': '09805-99999-01147-SDDEC', 'model': '16LS98FATW', 'manufactory': 'LENOVO', 'os_type': ('Windows',)},

        "mem":
            [
                {'manufacturer': 'Samsung', 'sn': '999B51DC', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelA-DIMM0'},
                {'manufacturer': 'Samsung', 'sn': '4844855C', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelB-DIMM0'}
            ],
        'disk':
            [
                { 'capacity': 238.4679079055786, 'sn': '2H848814191C',
                 'model': 'ADATA SU800NS38', 'manufacturer': '(标准磁盘驱动器)', 'slot': 1},
                { 'capacity': 465.7593083381653, 'sn': '5954TO10ZC',
                 'model': 'SanDisk SD8SB8U256G', 'manufacturer': '(标准磁盘驱动器)', 'slot': 0}
            ],
        'nic':
            [
                {'ipaddress': '', 'macaddress': '00:AC:39:5C:AA:19', 'model': '[00000001] VPN Client Adapter - VPN',
                 'name': 1, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '00:FF:AE:09:80:29', 'model': '[00000002] TAP-Windows Adapter V9',
                 'name': 2, 'netmask': ''},
                {'ipaddress': '192.168.8.15', 'macaddress': '48:E9:EF:9F:D7:AC',
                 'model': '[00000005] Realtek PCIe GBE Family Controller', 'name': 5,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '192.168.80.55', 'macaddress': 'A6:28:20:0D:66:2C',
                 'model': '[00000006] Qualcomm Atheros QCA61x4A Wireless Network Adapter', 'name': 6,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '', 'macaddress': 'FA:28:19:C0:99:23',
                 'model': '[00000007] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 7, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '0A:28:19:C0:99:23',
                 'model': '[00000008] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 8, 'netmask': ''},
                {'ipaddress': '', 'macaddress': 'F8:28:19:C0:99:24',
                 'model': '[00000010] Bluetooth Device (Personal Area Network)', 'name': 10, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '34:98:20:52:41:53', 'model': '[00000016] WAN Miniport (IP)',
                 'name': 16, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '40:DB:20:52:41:53', 'model': '[00000017] WAN Miniport (IPv6)',
                 'name': 17, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '4E:96:20:52:41:53',
                 'model': '[00000018] WAN Miniport (Network Monitor)', 'name': 18, 'netmask': ''}
            ],
    },

    {
        'cpu':
            {'cpu_count': 1, 'cpu_core_count': 2, 'cpu_model': 'Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz'},

        'basic':
            {'wake_up_type': 6, 'os_distribution': 'Microsoft', 'os_release': ('10 64bit  10.0.17134 ',),
             'sn': '09805-99999-01147-SDDED', 'model': '16LS98FATW', 'manufactory': 'LENOVO', 'os_type': ('Windows',)},

        "mem":
            [
                {'manufacturer': 'Samsung', 'sn': '999B51DD', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelA-DIMM0'},
                {'manufacturer': 'Samsung', 'sn': '4844855D', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelB-DIMM0'}
            ],
        'disk':
            [
                { 'capacity': 238.4679079055786, 'sn': '2H848814191D',
                 'model': 'ADATA SU800NS38', 'manufacturer': '(标准磁盘驱动器)', 'slot': 1},
                { 'capacity': 465.7593083381653, 'sn': '5954TO10ZD',
                 'model': 'SanDisk SD8SB8U256G', 'manufacturer': '(标准磁盘驱动器)', 'slot': 0}
            ],
        'nic':
            [
                {'ipaddress': '', 'macaddress': '00:AC:39:5C:AA:19', 'model': '[00000001] VPN Client Adapter - VPN',
                 'name': 1, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '00:FF:AE:09:80:29', 'model': '[00000002] TAP-Windows Adapter V9',
                 'name': 2, 'netmask': ''},
                {'ipaddress': '192.168.8.15', 'macaddress': '48:E9:EF:9F:D7:AD',
                 'model': '[00000005] Realtek PCIe GBE Family Controller', 'name': 5,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '192.168.80.55', 'macaddress': 'A6:28:20:0D:66:2D',
                 'model': '[00000006] Qualcomm Atheros QCA61x4A Wireless Network Adapter', 'name': 6,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '', 'macaddress': 'FA:28:19:C0:99:23',
                 'model': '[00000007] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 7, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '0A:28:19:C0:99:23',
                 'model': '[00000008] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 8, 'netmask': ''},
                {'ipaddress': '', 'macaddress': 'F8:28:19:C0:99:24',
                 'model': '[00000010] Bluetooth Device (Personal Area Network)', 'name': 10, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '34:98:20:52:41:53', 'model': '[00000016] WAN Miniport (IP)',
                 'name': 16, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '40:DB:20:52:41:53', 'model': '[00000017] WAN Miniport (IPv6)',
                 'name': 17, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '4E:96:20:52:41:53',
                 'model': '[00000018] WAN Miniport (Network Monitor)', 'name': 18, 'netmask': ''}
            ],
    },

    {
        'cpu':
            {'cpu_count': 1, 'cpu_core_count': 2, 'cpu_model': 'Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz'},

        'basic':
            {'wake_up_type': 6, 'os_distribution': 'Microsoft', 'os_release': ('10 64bit  10.0.17134 ',),
             'sn': '09805-99999-01147-SDDEE', 'model': '16LS98FATW', 'manufactory': 'LENOVO', 'os_type': ('Windows',)},

        "mem":
            [
                {'manufacturer': 'Samsung', 'sn': '999B51DE', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelA-DIMM0'},
                {'manufacturer': 'Samsung', 'sn': '4844855E', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelB-DIMM0'}
            ],
        'disk':
            [
                { 'capacity': 238.4679079055786, 'sn': '2H848814191E',
                 'model': 'ADATA SU800NS38', 'manufacturer': '(标准磁盘驱动器)', 'slot': 1},
                { 'capacity': 465.7593083381653, 'sn': '5954TO10ZE',
                 'model': 'SanDisk SD8SB8U256G', 'manufacturer': '(标准磁盘驱动器)', 'slot': 0}
            ],
        'nic':
            [
                {'ipaddress': '', 'macaddress': '00:AC:39:5C:AA:19', 'model': '[00000001] VPN Client Adapter - VPN',
                 'name': 1, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '00:FF:AE:09:80:29', 'model': '[00000002] TAP-Windows Adapter V9',
                 'name': 2, 'netmask': ''},
                {'ipaddress': '192.168.8.15', 'macaddress': '48:E9:EF:9F:D7:AE',
                 'model': '[00000005] Realtek PCIe GBE Family Controller', 'name': 5,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '192.168.80.55', 'macaddress': 'A6:28:20:0D:66:2E',
                 'model': '[00000006] Qualcomm Atheros QCA61x4A Wireless Network Adapter', 'name': 6,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '', 'macaddress': 'FA:28:19:C0:99:23',
                 'model': '[00000007] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 7, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '0A:28:19:C0:99:23',
                 'model': '[00000008] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 8, 'netmask': ''},
                {'ipaddress': '', 'macaddress': 'F8:28:19:C0:99:24',
                 'model': '[00000010] Bluetooth Device (Personal Area Network)', 'name': 10, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '34:98:20:52:41:53', 'model': '[00000016] WAN Miniport (IP)',
                 'name': 16, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '40:DB:20:52:41:53', 'model': '[00000017] WAN Miniport (IPv6)',
                 'name': 17, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '4E:96:20:52:41:53',
                 'model': '[00000018] WAN Miniport (Network Monitor)', 'name': 18, 'netmask': ''}
            ],
    },

    {
        'cpu':
            {'cpu_count': 1, 'cpu_core_count': 2, 'cpu_model': 'Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz'},

        'basic':
            {'wake_up_type': 6, 'os_distribution': 'Microsoft', 'os_release': ('10 64bit  10.0.17134 ',),
             'sn': '09805-99999-01147-SDDEE', 'model': '16LS98FATW', 'manufactory': 'LENOVO', 'os_type': ('Windows',)},

        "mem":
            [
                {'manufacturer': 'Samsung', 'sn': '999B51DE', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelA-DIMM0'},
                {'manufacturer': 'Samsung', 'sn': '4844855E', 'model': '物理内存', 'capacity': 8192.0,
                 'slot': 'ChannelB-DIMM0'}
            ],
        'disk':
            [
                { 'capacity': 238.4679079055786, 'sn': '2H848814191E',
                 'model': 'ADATA SU800NS38', 'manufacturer': '(标准磁盘驱动器)', 'slot': 1},
                { 'capacity': 465.7593083381653, 'sn': '5954TO10ZE',
                 'model': 'SanDisk SD8SB8U256G', 'manufacturer': '(标准磁盘驱动器)', 'slot': 0}
            ],
        'nic':
            [
                {'ipaddress': '', 'macaddress': '00:AC:39:5C:AA:1E', 'model': '[00000001] VPN Client Adapter - VPN',
                 'name': 1, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '00:FF:AE:09:80:2E', 'model': '[00000002] TAP-Windows Adapter V9',
                 'name': 2, 'netmask': ''},
                {'ipaddress': '192.168.8.15', 'macaddress': '48:E9:EF:9F:D7:AE',
                 'model': '[00000005] Realtek PCIe GBE Family Controller', 'name': 5,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '192.168.80.55', 'macaddress': 'A6:28:20:0D:66:2E',
                 'model': '[00000006] Qualcomm Atheros QCA61x4A Wireless Network Adapter', 'name': 6,
                 'netmask': ('255.255.255.0', '64')},
                {'ipaddress': '', 'macaddress': 'FA:28:19:C0:99:23',
                 'model': '[00000007] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 7, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '0A:28:19:C0:99:23',
                 'model': '[00000008] Microsoft Wi-Fi Direct Virtual Adapter', 'name': 8, 'netmask': ''},
                {'ipaddress': '', 'macaddress': 'F8:28:19:C0:99:24',
                 'model': '[00000010] Bluetooth Device (Personal Area Network)', 'name': 10, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '34:98:20:52:41:53', 'model': '[00000016] WAN Miniport (IP)',
                 'name': 16, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '40:DB:20:52:41:53', 'model': '[00000017] WAN Miniport (IPv6)',
                 'name': 17, 'netmask': ''},
                {'ipaddress': '', 'macaddress': '4E:96:20:52:41:53',
                 'model': '[00000018] WAN Miniport (Network Monitor)', 'name': 18, 'netmask': ''}
            ],
    },

]

for pc in pcs:

    sn = pc['basic']['sn']
    cpu_count = pc['cpu']['cpu_count']
    cpu_physical_count = pc['cpu']['cpu_core_count']
    cpu_model = pc['cpu']['cpu_model']
    model = pc['basic']['model']
    manufacturer = pc['basic']['manufactory']


    host = Host(sn=sn, cpu_count=cpu_count, cpu_physical_count=cpu_physical_count, cpu_model=cpu_model,
                manufacturer=manufacturer, model=model)
    host.number = Host.objects.all().count() + 1
    host.save()

    for mem in pc['mem']:
        m = Memory(**mem)
        m.host_obj = host
        m.save()

    for disk in pc['disk']:
        d = Disk(**disk)
        d.host_obj = host
        d.save()

    for nic in pc['nic']:
        n = NIC(**nic)
        n.host_obj = host
        n.save()



