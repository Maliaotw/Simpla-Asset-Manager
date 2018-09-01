from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
import hashlib
# Create your views here.

ck = "mdfmsijfiosdjoidfjdf"

@csrf_exempt
def asset(request):


    # print(request.POST)
    # print(request.body)
    if request.method == 'POST':


        auth_key_time = request.META["HTTP_AUTHKEY"]

        auth_key,client_ctime = auth_key_time.split("|")
        key_time = "%s|%s" % (ck,client_ctime)
        m = hashlib.md5()
        m.update(bytes(key_time, encoding='utf-8'))
        authkey = m.hexdigest()

        host_info = json.loads(str(request.body,encoding='utf8'))
        if request.META['HTTP_AUTHKEY'] == ck:
            ret = '...'
        else:
            ret = "驗證失敗"


        print(host_info)

        return HttpResponse(ret)








