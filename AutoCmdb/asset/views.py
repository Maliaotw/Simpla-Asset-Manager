from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from asset import models
from asset import forms


# Create your views here.

def index(request):
    asset_obj = models.Asset.objects.all()
    category_obj = models.Catagory.objects.all()
    department_obj = models.Department.objects.all()
    user_obj = models.UserProfile.objects.all()


    if request.method == 'POST':

        data = {
            'msg': '',
            'status': ''
        }

        print(request.POST)

        '''
        {'sn': ['040'], 'user': ['807'], 'department': ['7'], 'price': ['400'], 'category': ['2']}>

        '''

        form_obj = forms.AssetForm(data=request.POST)

        if form_obj.is_valid():
            # print(form_obj)

            manager = form_obj.cleaned_data['manager']
            sn = form_obj.cleaned_data['sn']
            category = form_obj.cleaned_data['category']
            dent = form_obj.cleaned_data['department']
            price = form_obj.cleaned_data['price']

            models.Asset.objects.create(manager=manager, sn=sn, category=category, department=dent,
                                        price=price)

            data['status'] = 'ok'
            data['msg'] = '新增成功'

        else:
            data['status'] = 'error'
            data['msg'] = '輸入錯誤'

        return JsonResponse(data)

    return render(request, "asset/index.html", locals())


def department(request):
    department_obj = models.Department.objects.all()
    return render(request, "asset/department.html", locals())


def category(request):
    category_obj = models.Catagory.objects.all()
    return render(request, "asset/category.html", locals())


def user(request):
    user_obj = models.UserProfile.objects.all()
    return render(request, 'user/index.html', locals())
