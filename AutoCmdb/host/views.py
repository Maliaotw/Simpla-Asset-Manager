from django.shortcuts import render, HttpResponse
from host import models
from asset.models import Location

# Create your views here.
def index(requesrt):
    host_obj = models.Host.objects.all()

    data = {'host_obj': host_obj}

    return render(requesrt, "host/index.html", data)

def location(requesrt):
    local_obj = Location.objects.all()

    data = {'local_obj': local_obj}

    return render(requesrt, "host/location.html", data)




def demo1(request):
    return render(request, "base.html")