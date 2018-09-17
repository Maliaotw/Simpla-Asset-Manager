from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
import hashlib
import time
from asset.models import Catagory ,Asset
# Create your views here.

ck = "mdfmsijfiosdjoidfjdf"
auth_list = []

@csrf_exempt
def asset(request):

    if request.method == 'POST':

        print(request.META)
        auth_key_time = request.META["HTTP_AUTH_KEY"]

        auth_key_client,client_ctime = auth_key_time.split("|")
        server_current_time = time.time()
        if server_current_time-30 > float(client_ctime):
            # 太久遠
            return HttpResponse("驗證失敗")
        if auth_key_time in auth_list:
            # 已經訪問過
            return HttpResponse("你來晚了")

        # 開始驗證

        key_time = "%s|%s" % (ck,client_ctime)
        m = hashlib.md5()
        m.update(bytes(key_time, encoding='utf-8'))
        authkey = m.hexdigest()


        if authkey != auth_key_client:
            return HttpResponse("授權失敗")
        auth_list.append(auth_key_time)

        print("auth_list",auth_list)

        return HttpResponse("成功")


def category(request):
    cate_id = request.GET.get('cate')
    c = Catagory.objects.get(id=cate_id)
    a = Asset.objects.filter(category=c)
    data = {
        'count':a.count(),
        'number':"%03d" % a.count()
    }
    return JsonResponse(data)

