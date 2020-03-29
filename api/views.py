from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import hashlib
import time
from asset.models import Category, Asset, Department, UserProfile, AssetRepairDetail
from host.models import Host, Memory, Disk, NIC, HostRecord
from django.conf import settings
import pytz


# Create your views here.

ck = "mdfmsijfiosdjoidfjdf"
auth_list = []

modeldata = {
    '20H5A036TW': 'E570',
    '20C6A05FTW': 'E540',
    '20LX000DTW': 'L580',
    '20150': 'G580'
}


@csrf_exempt
def asset_no_hostname(request):
    '''
    自增資產
    :param request:
    :return:
    '''
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
        print(request.body)
        data = eval(json.loads(request.body))

        #  Mem Nic Disk Basic Cpu

        mems = data['mem']
        print(mems)
        nics = data['nic']
        disks = data['disk']
        basic = data['basic']
        cpu = data['cpu']

        # --- 找出網卡IP與來源IP一致的MAC位址
        nic_macs = [nic.get('macaddress') for nic in data['nic']]

        # --- 對網卡mac與資料庫相符的筆數
        hosts = Host.objects.filter(nic__macaddress__in=nic_macs)

        host_dict = {}
        host_dict.update(cpu)
        host_dict.update(basic)
        hostname = host_dict.pop('hostname')

        if hosts:  # 有編號就更新
            host_obj = hosts.first()
            host_obj.manage_ip = remote_ip
            # print(host_obj)

            for k, v in host_dict.items():
                setattr(host_obj, k, v)
            host_obj.save()

        else:  # 自動編上最新編號
            host_obj = Host(manage_ip=remote_ip, **host_dict)

            host_obj.number = Host.objects.all().count() + 1
            num_format = "%03d" % (host_obj.number)
            name = "%s-%s" % ("PC", num_format)
            host_obj.name = name
            host_obj.manage_ip = remote_ip
            host_obj.save()

        # print(host_obj.number)
        # print(host_obj.name)
        # print(disks)

        for mem in mems:

            m = Memory.objects.filter(model=mem['model'])
            if m:
                print(m)
                m_obj = m.first()
                m_obj.host_obj = host_obj
                m_obj.save()
            else:
                m_obj = Memory(**mem)
                m_obj.host_obj = host_obj
                m_obj.save()

        for disk in disks:

            d = Disk.objects.filter(model=disk['model'])
            if d:
                d_obj = d.first()
                d_obj.host_obj = host_obj
                d_obj.save()
            else:
                d_obj = Disk(**disk)
                d_obj.host_obj = host_obj
                d_obj.save()

        for nic in nics:

            n = NIC.objects.filter(model=nic['model'])
            if n:
                n_obj = n.first()
                n_obj.host_obj = host_obj
                n_obj.save()
            else:
                n_obj = NIC(**nic)
                n_obj.host_obj = host_obj
                n_obj.save()

        return HttpResponse("成功")


@csrf_exempt
def asset_by_hostname(request):
    '''
    根據電腦名稱 新增/更新資產
    :param request:
    :return:
    '''
    if request.method == 'GET':

        remote_ip = request.META['REMOTE_ADDR']
        print(remote_ip)
        # print(request.META)
        # print(request.META['REMOTE_ADDR'])
        # print(request.META['REMOTE_HOST'])
        return HttpResponse("GET")

    elif request.method == 'POST':

        ret = {
            'code': '',
            'status': '',
            'msg': '',
            'data': {'mems': [], 'nics': [], 'disks': [], 'record': ''}
        }

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
        # print(mems)
        nics = data['nic']
        disks = data['disk']
        basic = data['basic']
        cpu = data['cpu']

        '''
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
        '''

        # 以host_dict的hostname當作電腦編號
        host_dict = {}
        host_dict.update(cpu)
        host_dict.update(basic)
        # print(host_dict)

        # --- 對電腦編號與資料庫相符的筆數
        hostname = host_dict.pop('hostname')

        host_dict['model'] = modeldata.get(host_dict['model']) if modeldata.get(host_dict['model']) else host_dict[
            'model']
        print('host_dict', host_dict)

        hosts = Host.objects.filter(name=hostname)
        print("HOST", hosts)
        if hosts:  # 有編號就更新
            host_obj = hosts.first()
            host_obj.name = hostname
            host_obj.manage_ip = remote_ip
            # print(host_obj)
            for k, v in host_dict.items():
                setattr(host_obj, k, v)
            host_obj.save()



        else:  # 自動編上最新編號
            host_obj = Host(manage_ip=remote_ip, **host_dict)
            host_obj.number = hostname.split('-')[1]
            host_obj.manage_ip = remote_ip
            host_obj.name = hostname
            # print(host_dict)
            # print(host_obj)
            host_obj.save()

            ret['status'] = 'ADD PC'
        print("HOST")

        nics_obj = []
        for nic in nics:
            n = NIC.objects.filter(model=nic['model'], ipaddress=nic['ipaddress'])
            if n:
                n_obj = n.first()

                if n_obj in host_obj.nic.all():
                    pass
                else:
                    # print('更新')
                    ret['status'] = 'UPDATE'
                    ret['data']['nics'].append('更新 %s %s' % (n_obj.model, n_obj.macaddress))
                n_obj.host_obj = host_obj
                n_obj.save()

            else:  # 新增 (資料庫未出現的內存
                # print(nic)
                n_obj = NIC(**nic)
                n_obj.host_obj = host_obj
                n_obj.save()
                # print('新增')
                ret['data']['nics'].append('新增 %s %s' % (n_obj.model, n_obj.macaddress))

            nics_obj.append(n_obj)
        print("NIC")

        # print(nics_obj)

        # 沒有被匹配到的 (刪除
        for i in host_obj.nic.all():
            if i in nics_obj:
                pass
            else:
                i.delete()
                ret['data']['nics'].append('移除 %s %s' % (i.model, i.macaddress))

        # print(ret['data']['nics'])

        # 内存
        mems_obj = []
        for mem in mems:
            m = Memory.objects.filter(sn=mem['sn'])
            print(m)
            if m:
                print('存在', m)
                m_obj = m.first()

                if m_obj in host_obj.memory.all():
                    pass
                else:
                    # print('更新')
                    ret['status'] = 'UPDATE'
                    ret['data']['mems'].append('更新 %s %s' % (m_obj.model, m_obj.capacity))

                m_obj.host_obj = host_obj
                m_obj.save()
            else:
                print('新增', m)
                m_obj = Memory(**mem)
                m_obj.host_obj = host_obj
                m_obj.save()
                # print('新增')
                ret['data']['mems'].append('新增 %s %s' % (m_obj.model, m_obj.capacity))

            mems_obj.append(m_obj)

        # print(mems_obj)

        # 沒有被匹配到的 (刪除
        for i in host_obj.memory.all():
            if i in mems_obj:
                pass
            else:
                i.delete()
                ret['data']['mems'].append('移除 %s %s' % (i.model, i.capacity))

        print("MEM")

        # 硬盤

        disks_obj = []
        for disk in disks:

            d = Disk.objects.filter(sn=disk['sn'])
            if d:
                d_obj = d.first()

                if d_obj in host_obj.disk.all():
                    pass
                else:
                    # print('更新')
                    ret['status'] = 'UPDATE'
                    ret['data']['disks'].append('更新 %s %s' % (d_obj.model, d_obj.capacity))

                d_obj.host_obj = host_obj
                d_obj.save()
            else:
                d_obj = Disk(**disk)
                d_obj.host_obj = host_obj
                d_obj.save()
                # print('新增')
                ret['data']['disks'].append('新增 %s %s' % (d_obj.model, d_obj.capacity))

            disks_obj.append(d_obj)

        # 沒有被匹配到的 (刪除
        for i in host_obj.disk.all():
            if i in disks_obj:
                pass
            else:
                i.delete()
                ret['data']['disks'].append('移除 %s %s' % (i.model, i.capacity))

        # print(ret['data']['disks'])

        # 返回前 Msg 處理 新增主機更變紀錄

        if ret['status'] == 'ADD PC':
            ret['data']['record'] = "新增主機"
        elif ret['status'] == 'UPDATE':
            data = ret['data']
            ret['data']['record'] = ""
            for key in list(data.keys()):
                ret['data']['record'] += "%s:\n\n" % key
                ret['data']['record'] += '\n'.join(data[key])
                ret['data']['record'] += '\n\n'

        if ret['data']['record']:
            HostRecord.objects.create(
                host_obj=host_obj,
                title='%s update' % time.strftime("%Y%m%d"),
                summary=ret['data']['record']
            )

        # 返回
        print('成功')
        ret['code'] = 200
        ret['msg'] = '成功'
        return JsonResponse(ret)


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
    if dent_id:
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


def ardtohtml(request):
    '''
    資產報修詳細
    asset_repair_detail
    :param request:
    :return:
    '''

    ret = {'status': '', 'code': '', 'msg': '', 'data': {}}

    if request.method == 'GET':

        id = request.GET.get('id')

        ard_objs = AssetRepairDetail.objects.filter(repair_id=id)

        print(ard_objs)

        html = '<div id="reply">'

        Shanghai = pytz.timezone(settings.TIME_ZONE)

        for ard in ard_objs:
            t = ard.create_date.astimezone(Shanghai)
            html += '<div class="panel panel-primary">'
            html += '<div class="panel-heading">'
            html += '<strong><i class="far fa-user"></i>%s</strong></div>' % ard.user.code
            html += '<div class="panel-body">'
            html += '<span>%s</span>' % ard.content
            html += '<p class="text-right">%s</p>' % t.strftime("%Y/%m/%d %H:%M")
            html += '</div></div>'
        html += "</div>"

        ret['status'] = 'ok'
        ret['code'] = 200
        ret['msg'] = '返回hrml'
        ret['data'] = html

        return JsonResponse(ret)



    else:
        return JsonResponse(ret)
