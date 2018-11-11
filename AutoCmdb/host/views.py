from django.shortcuts import render, HttpResponse
from host import models
from asset.models import Location,UserProfile,Asset
from host import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def host(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    search_field = {}

    host_obj = models.Host.objects.all()

    host_obj1 = models.Host.objects.filter(asset__isnull=True).all().select_related('asset')
    host_exclude_objs = models.Host.objects.exclude(asset__isnull=True).all()
    asset_host_obj = [i.asset for i in host_exclude_objs]

    asset_pc= Asset.objects.filter(category__name="電腦").all()
    asset_host_obj = list(filter(lambda x:x not in asset_host_obj,asset_pc))



    it_user_obj = UserProfile.objects.filter(dent__name='資訊').all()



    # 分頁功能

    paginator = Paginator(host_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        host_obj = paginator.page(page)
    except PageNotAnInteger:
        host_obj = paginator.page(1)
    except EmptyPage:
        host_obj = paginator.page(paginator.num_pages)


    return render(request, "host/index.html", locals())




def host_info(request,pk):

    host_obj = models.Host.objects.get(id=pk)

    host_form_obj = forms.HostForm(instance=host_obj)

    nic_forms_obj = [forms.NICForm(instance=nic) for nic in host_obj.nic.all()]

    disk_forms_obj = [forms.DiskForm(instance=disk) for disk in host_obj.disk.all()]

    mem_forms_obj = [forms.MemoryForm(instance=memory) for memory in host_obj.memory.all()]


    return render(request, "host/host_info.html", locals())


def location(requesrt):
    local_obj = Location.objects.all()

    data = {'local_obj': local_obj}

    return render(requesrt, "host/location.html", data)



def demo1(request):
    return render(request, "base.html")