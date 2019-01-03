from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from host import models
from asset.models import Location, UserProfile, Asset, Category, Department,AssetRecord,AssetRepair,AssetRepairDetail
from host import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict


# Create your views here.
def host(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':
        search_field = {}

        # host_obj = models.Host.objects.all()
        it_user_obj = UserProfile.objects.filter(dent__name='資訊').all()
        location_obj = Location.objects.all()

        status_field = models.Host.status_choice
        department_obj = Department.objects.all()

        # GET 字段
        name = request.GET.get("name", '')
        status = request.GET.get("status", '')
        dent_id = request.GET.get("dent_id", '')

        search_field['name'] = name
        search_field['status'] = status
        search_field['dent_id'] = dent_id

        # GET 字段 篩選
        print('search_field', search_field)

        if status and dent_id:
            host_obj = models.Host.objects.filter(name__contains=name,status__contains=status,asset__department_id=dent_id)
        elif status:
            host_obj = models.Host.objects.filter(name__contains=name,status__contains=status)
        elif dent_id:
            host_obj = models.Host.objects.filter(name__contains=name,asset__department_id=dent_id)
        elif name:
            host_obj = models.Host.objects.filter(name__contains=name)
        else:
            host_obj = models.Host.objects.all()



        # 分頁功能
        paginator = Paginator(host_obj, 10)  # Show 10 contacts per page

        page = request.GET.get('page')
        try:
            host_obj = paginator.page(page)
        except PageNotAnInteger:
            host_obj = paginator.page(1)
        except EmptyPage:
            host_obj = paginator.page(paginator.num_pages)

    if request.method == 'PUT':
        put = QueryDict(request.body)
        print(put)
        id = put.get('id')
        status = put.get('status')
        ops_owner = put.get('ops_owner')
        asset = put.get('asset')
        location = put.get('location')

        host_obj = models.Host.objects.get(id=id)
        host_obj.status = status
        host_obj.location = Location.objects.get(id=location)
        host_obj.ops_owner = UserProfile.objects.get(id=ops_owner)
        host_obj.asset = Asset.objects.get(id=asset)
        host_obj.save()

        ret['status'] = 'ok'

        return JsonResponse(ret)

    return render(request, "host/index.html", locals())


def host_info(request, pk):
    host_obj = models.Host.objects.get(id=pk)
    host_form_obj = forms.HostForm(instance=host_obj)
    nic_forms_obj = [forms.NICForm(instance=nic) for nic in host_obj.nic.all()]
    disk_forms_obj = [forms.DiskForm(instance=disk) for disk in host_obj.disk.all()]
    mem_forms_obj = [forms.MemoryForm(instance=memory) for memory in host_obj.memory.all()]

    asset_record_obj = AssetRecord.objects.filter(asset_obj__Host=host_obj)
    # print(asset_record_obj)
    asset_repair_obj = AssetRepair.objects.filter(asset_obj__Host=host_obj)

    asset_repair_detail = AssetRepairDetail.objects.filter(repair=asset_repair_obj)

    return render(request, "host/host_info.html", locals())


def host_input(request):
    return render(request, "host/input.html", locals())







def host_output(request):
    host_obj = models.Host.objects.all()
    return render(request, "host/output.html", locals())









def location(requesrt):
    local_obj = Location.objects.all()
    data = {'local_obj': local_obj}
    return render(requesrt, "host/location.html", data)


def demo1(request):
    return render(request, "base.html")
