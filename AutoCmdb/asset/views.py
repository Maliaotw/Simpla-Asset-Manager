from django.shortcuts import render, HttpResponse
from asset import models
from asset import froms


# Create your views here.

def index(request):
    asset_obj = models.Asset.objects.all()


    data = {
        'asset_obj': asset_obj,
    }

    return render(request, "asset/index.html", data)
