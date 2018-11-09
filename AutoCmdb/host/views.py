from django.shortcuts import render, HttpResponse
from host import models
from asset.models import Location
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
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

def location(requesrt):
    local_obj = Location.objects.all()

    data = {'local_obj': local_obj}

    return render(requesrt, "host/location.html", data)



def demo1(request):
    return render(request, "base.html")