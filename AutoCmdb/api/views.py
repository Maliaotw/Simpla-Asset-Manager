from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import hashlib
import time
from asset.models import Category, Asset, Department, UserProfile
from host.models import Host, Memory, Disk, NIC

# Create your views here.

ck = "mdfmsijfiosdjoidfjdf"
auth_list = []



@csrf_exempt
def asset_no_hostname(request):
    if request.method == 'GET':
        print(request.META)

        print(request.META['REMOTE_ADDR'])
        return HttpResponse("GET")


    elif request.method == 'POST':

        # print(request.META)
        auth_key_time = request.META["HTTP_AUTH_KEY"]

        auth_key_client, client_ctime = auth_key_time.split("|")
        server_current_time = time.time()
        if server_current_time - 30 > float(client_ctime):
            # 太久遠
            return HttpResponse("驗證失敗")
        if auth_key_time in auth_list:
            # 已經訪問過
            return HttpResponse("你來晚了")

        # 開始驗證
        key_time = "%s|%s" % (ck, client_ctime)
        m = hashlib.md5()
        m.update(bytes(key_time, encoding='utf-8'))
        authkey = m.hexdigest()

        if authkey != auth_key_client:
            return HttpResponse("授權失敗")
        auth_list.append(auth_key_time)

        # print("auth_list", auth_list)

        remote_ip = request.META['REMOTE_ADDR']
        # print('remote_ip',remote_ip)

        # 獲取主機JSON
        # print(request.body)
        # data = json.loads(request.body)

        data = eval(json.loads(request.body))

        #  Mem Nic Disk Basic Cpu

        mems = data['mem']
        nics = data['nic']
        disks = data['disk']
        basic = data['basic']
        cpu = data['cpu']

        # --- 找出網卡IP與來源IP一致的MAC位址

        nic_macs = []

        for nic in data['nic']:
            ipaddress = nic.get('ipaddress')
            macaddress = nic.get('macaddress')

            # 網卡mac
            nic_macs.append(macaddress)

            # --- 與來源IP相符的網卡

            if ipaddress == remote_ip:
                print(ipaddress)
                print(macaddress)

        # --- 對網卡mac與資料庫相符的筆數
        hosts = Host.objects.filter(nic__macaddress__in=nic_macs)

        # print('cpu',cpu)
        # print('basic',basic)

        host_dict = {}
        host_dict.update(cpu)
        host_dict.update(basic)

        if hosts: # 有編號就更新
            host_obj = hosts.first()
            # print(host_obj)

            for k,v in host_dict.items():
                setattr(host_obj, k, v)

        else: # 自動編上最新編號
            host_obj = Host(manage_ip=ipaddress,**host_dict)

            host_obj.number = Host.objects.all().count() + 1
            num_format = "%03d" % (host_obj.number)
            name = "%s-%s" % ("PC", num_format)
            host_obj.name = name
            host_obj.save()

        # print(host_obj.number)
        # print(host_obj.name)
        # print(disks)

        for mem in mems:
            m = Memory(**mem)
            m.host_obj = host_obj
            m.save()

        for disk in disks:
            d = Disk(**disk)
            d.host_obj = host_obj
            d.save()

        for nic in nics:
            n = NIC(**nic)
            n.host_obj = host_obj
            n.save()

        return HttpResponse("成功")



@csrf_exempt
def asset_by_hostname(request):
    if request.method == 'GET':
        print(request.META)

        print(request.META['REMOTE_ADDR'])
        print(request.META['REMOTE_HOST'])

        return HttpResponse("GET")


    elif request.method == 'POST':

        # print(request.META)
        auth_key_time = request.META["HTTP_AUTH_KEY"]

        auth_key_client, client_ctime = auth_key_time.split("|")
        server_current_time = time.time()
        if server_current_time - 30 > float(client_ctime):
            # 太久遠
            return HttpResponse("驗證失敗")
        if auth_key_time in auth_list:
            # 已經訪問過
            return HttpResponse("你來晚了")

        # 開始驗證
        key_time = "%s|%s" % (ck, client_ctime)
        m = hashlib.md5()
        m.update(bytes(key_time, encoding='utf-8'))
        authkey = m.hexdigest()

        if authkey != auth_key_client:
            return HttpResponse("授權失敗")
        auth_list.append(auth_key_time)

        # print("auth_list", auth_list)

        remote_ip = request.META['REMOTE_ADDR']


        # print('remote_ip',remote_ip)

        # 獲取主機JSON
        # print(request.body)
        # data = json.loads(request.body)


        return HttpResponse("成功")



def category(request):
    cate_id = request.GET.get('cate')

    c = Category.objects.get(id=cate_id)
    a = Asset.objects.filter(category=c).count() + 1
    number = "%03d" % a

    data = {
        'count': a,
        'number': number,
        'name': "%s-%s" % (c.code, number)
    }
    return JsonResponse(data)


def dent_user(request):
    '''
    前端選擇部門返回關聯所有部門用戶
    :param request:
    :return:
    '''

    ret = {
        'msg': '',
        'users': '',
        'owner': ''
    }

    dent_id = request.GET.get('dent')

    dent = Department.objects.get(id=dent_id)
    users = UserProfile.objects.filter(dent=dent)

    # print(dent)
    # print(dent.user)
    # print(users)

    # 負責人
    user_list = []

    if dent.user:
        ret['owner'] = dent.user.user.id
        if dent.user.dent == dent:
            pass
        else:
            user_data = {
                'name': "%s(%s)" % (dent.user.code, dent.user.name),
                'id': dent.user.user.id
            }
            user_list.append(user_data)

    # 遍歷用戶

    for u in users:
        user_data = {
            'name': "%s(%s)" % (u.code, u.name),
            'id': u.user.id
        }
        user_list.append(user_data)

    ret['users'] = user_list

    return JsonResponse(ret)


def add_user_number(request):
    ret = {
        'data': '',
        'status': ''
    }

    dent_id = request.GET.get('id')

    if dent_id:

        dent_obj = Department.objects.get(id=dent_id)

        # 部門人數
        user_count = UserProfile.objects.filter(dent_id=dent_id).count() + 1

        # 部門編號
        block_number = dent_obj.block_number

        # 部門長度

        block_number_len = dent_obj.block_number_len

        num_format = "%0{}d".format(block_number_len - len(block_number))  # block_numer_len

        num = num_format % (user_count)  # block_numer

        print("block_number + num", block_number + num)
        ret['data'] = block_number + num
        ret['status'] = 'ok'

    else:
        ret['data'] = ""
        ret['status'] = 'error'

    # test

    return JsonResponse(ret)


def host(request):
    ret = {
        'data': '',
        'status': '',
        'own': ''
    }

    if request.method == 'GET':

        host_id = request.GET.get('hostid')
        asset_id = request.GET.get('assetid')

        print('host', host_id)
        print('asset', asset_id)

        # 有綁定主機的資產
        asset_include_hosts = [i.asset for i in Host.objects.exclude(asset__isnull=True).all()]
        print('asset_include_hosts', asset_include_hosts)

        # 篩選只有主機的資產
        asset_obj = Asset.objects.filter(category__name="電腦").all()

        # 篩選出未綁定主機的資產
        asset_exclude_hosts = list(filter(lambda x: x not in asset_include_hosts, asset_obj))
        print('asset_exclude_hosts', asset_exclude_hosts)

        # 當前主機 若有綁定資產將再加入一筆已綁定資產
        host_obj = Host.objects.get(id=host_id)

        if host_obj.asset:
            print('有綁')
            asset_exclude_hosts.append(host_obj.asset)
            ret['own'] = host_obj.asset.id
        else:
            print('沒綁')

        print(asset_exclude_hosts)

        asset_list = []
        for asset in asset_exclude_hosts:
            asset_data = {
                'asset': str(asset),
                'id': asset.id
            }
            asset_list.append(asset_data)
        ret['data'] = asset_list

        return JsonResponse(ret)
