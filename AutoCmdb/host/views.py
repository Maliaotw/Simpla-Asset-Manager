from django.shortcuts import render, HttpResponse
from host import models
from asset.models import Location
from host import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def host(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    search_field = {}

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


    return render(request, "host/index.html", locals())




def host_info(request,pk):

    host_obj = models.Host.objects.get(id=pk)

    host_form_obj = forms.HostForm(instance=host_obj)

    print(host_form_obj)


    print(host_obj.nic.all())
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