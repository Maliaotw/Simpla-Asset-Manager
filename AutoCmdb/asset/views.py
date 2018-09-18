from django.shortcuts import render, HttpResponse
from asset import models
from asset import froms


# Create your views here.

def index(request):
    asset_obj = models.Asset.objects.all()
    category_obj = models.Catagory.objects.all()
    department_obj = models.Department.objects.all()
    user_obj = models.UserProfile.objects.all()

    if request.method == 'POST':
        print(request.POST)
        return HttpResponse('POST ok')

    return render(request, "asset/index.html",locals())

def department(request):
    department_obj = models.Department.objects.all()
    return render(request, "asset/department.html",locals())

def category(request):
    category_obj = models.Catagory.objects.all()
    return render(request, "asset/category.html",locals())

def user(request):
    user_obj = models.UserProfile.objects.all()
    return render(request,'user/index.html',locals())






