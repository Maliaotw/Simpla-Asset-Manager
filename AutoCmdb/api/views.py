from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import hashlib
import time
from asset.models import Catagory, Asset, Department, UserProfile

# Create your views here.

ck = "mdfmsijfiosdjoidfjdf"
auth_list = []


@csrf_exempt
def asset(request):
    if request.method == 'POST':

        print(request.META)
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

        print("auth_list", auth_list)

        return HttpResponse("成功")


def category(request):
    cate_id = request.GET.get('cate')

    c = Catagory.objects.get(id=cate_id)
    a = Asset.objects.filter(category=c).count() + 1
    data = {
        'count': a,
        'number': "%03d" % a
    }
    return JsonResponse(data)


def dent_user(request):
    ret = {
        'msg': '',
        'users': '',
        'owner': ''
    }

    dent_id = request.GET.get('dent')

    dent = Department.objects.get(id=dent_id)
    users = UserProfile.objects.filter(dent=dent)
    # print(users)

    # 負責人

    if dent.user:
        ret['owner'] = {
            'user': dent.user.name,
            'code': '%s%s' % (dent.block_number, dent.user.code),
            'id': dent.user.user.id,
        }

    # 遍歷用戶
    user_list = []
    for u in users:
        user_data = {
            'user': u.name,
            'code': "%s%s" % (dent.block_number, u.code),
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
    dent_obj = Department.objects.get(id=dent_id)

    # 部門人數
    user_count = UserProfile.objects.filter(dent=dent_obj).count()+1

    # 部門編號
    block_number = dent_obj.block_number

    # 部門長度

    block_number_len = dent_obj.block_number_len

    num_format = "%0{}d".format(block_number_len - len(block_number))  # block_numer_len

    num = num_format % (user_count)  # block_numer

    print(block_number + num)
    ret['data'] = block_number + num

    return JsonResponse(ret)

