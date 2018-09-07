from django.shortcuts import render, HttpResponse
from asset import models
from asset import froms


# Create your views here.

def index(request):
    asset_obj = models.AssetHost.objects.all()
    asset_form = froms.AssetForm()
    assethost_form = froms.AssetHostForm()

    data = {
        'asset_obj': asset_obj,
        'asset_form': asset_form,
        'assethost_form': assethost_form
    }

    return render(request, "asset/index.html", data)
