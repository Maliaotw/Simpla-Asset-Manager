from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
from asset import models
from asset import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    search_field = {}

    category_obj = models.Catagory.objects.all()
    department_obj = models.Department.objects.all()
    user_obj = models.UserProfile.objects.all()

    if request.GET:

        # GET 字段
        name = request.GET.get("name", '')
        cate_id = request.GET.get("cate_id", '')
        dent_id = request.GET.get("dent_id", '')

        search_field['name'] = name
        search_field['cate_id'] = cate_id
        search_field['dent_id'] = dent_id

        print(search_field)

        # GET 字段 篩選

        if cate_id and dent_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name, category_id=cate_id, department_id=dent_id)
        elif cate_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name, category_id=cate_id)
        elif dent_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name, department_id=dent_id)
        else:
            asset_obj = models.Asset.objects.filter(sn__contains=name)

    else:
        asset_obj = models.Asset.objects.all()

    # 分頁功能

    paginator = Paginator(asset_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        asset_obj = paginator.page(page)
    except PageNotAnInteger:
        asset_obj = paginator.page(1)
    except EmptyPage:
        asset_obj = paginator.page(paginator.num_pages)

    if request.method == 'POST':

        ret = {
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

            models.Asset.objects.create(manager=manager, sn=sn, category=category, department=dent, price=price)

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '新增信息輸入不正確!'

        return JsonResponse(ret)

    if request.method == 'PUT':
        print("This is PUT")
        ret = {"status": "", "re_html": "", "msg": ""}

        put = QueryDict(request.body)
        print(put)
        id = put.get('id')
        asset_obj = models.Asset.objects.get(id=id)

        form_obj = forms.AssetForm(data=put, instance=asset_obj)
        if form_obj.is_valid():

            category = form_obj.cleaned_data['category']
            department = form_obj.cleaned_data['department']
            manager = form_obj.cleaned_data['manager']
            price = form_obj.cleaned_data['price']
            purchase_date = form_obj.cleaned_data['purchase_date']

            asset_obj.category = category
            asset_obj.department = department
            asset_obj.manager = manager
            asset_obj.price = price
            asset_obj.purchase_date = purchase_date
            asset_obj.save()

            ret['status'] = "ok"


        else:
            ret['status'] = 'error'

        return JsonResponse(ret)

    return render(request, "asset/index.html", locals())


def department(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    search_field = {}

    department_obj = models.Department.objects.all()
    user_obj = models.UserProfile.objects.all()

    # 分頁功能

    paginator = Paginator(department_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        dent_obj = paginator.page(page)
    except PageNotAnInteger:
        dent_obj = paginator.page(1)
    except EmptyPage:
        dent_obj = paginator.page(paginator.num_pages)

    if request.method == 'POST':

        form_obj = forms.DentForm(data=request.POST)

        if form_obj.is_valid():

            form_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '新增信息輸入不正確!'

        return JsonResponse(ret)

    if request.method == 'PUT':
        print("This is PUT")

        put = QueryDict(request.body)
        print(put)
        dent_id = put.get('id')
        dent_obj = models.Department.objects.get(id=dent_id)
        user_id = put.get('user')

        if user_id:
            user_obj = models.UserProfile.objects.get(id=user_id)
            dent_obj.user = user_obj
        else:

            dent_obj.user = None

        dent_obj.save()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)

    if request.method == 'DELETE':
        print("This is Delete")
        put = QueryDict(request.body)
        id = put.get('id')
        dent_obj = models.Department.objects.get(id=id)
        dent_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)

    return render(request, "asset/department.html", locals())


def category(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    search_field = {}

    category_obj = models.Catagory.objects.all()

    # 分頁功能

    paginator = Paginator(category_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        cary_obj = paginator.page(page)
    except PageNotAnInteger:
        cary_obj = paginator.page(1)
    except EmptyPage:
        cary_obj = paginator.page(paginator.num_pages)

    # 增
    if request.method == 'POST':

        print("This is POST")

        form_obj = forms.CaryForm(data=request.POST)

        if form_obj.is_valid():

            form_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '輸入錯誤!'

        return JsonResponse(ret)

    # 改
    if request.method == 'PUT':

        print("This is PUT")

        put = QueryDict(request.body)
        print(put)
        cary_id = put.get('id')
        name = put.get('name')
        code = put.get('code')

        cary_obj = models.Catagory.objects.get(id=cary_id)

        form_obj = forms.CaryForm(data=put, instance=cary_obj)

        if form_obj.is_valid():
            form_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '修改成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '修改信息輸入不正確!'

        return JsonResponse(ret)

    # 刪
    if request.method == 'DELETE':
        print("This is Delete")
        put = QueryDict(request.body)
        id = put.get('id')

        print(put)

        cary_obj = models.Catagory.objects.get(id=id)
        cary_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)

    return render(request, "asset/category.html", locals())


def user(request):
    ret = {"status": "", "re_html": "", "msg": ""}
    search_field = {}

    user_obj = models.UserProfile.objects.all()
    sex_obj = models.UserProfile.sex_choice

    # print(sex_obj)

    dent_obj = models.Department.objects.all()

    # user forms表單
    form_obj = forms.User_Add_Form()

    if request.GET:
        # GET 字段
        name = request.GET.get("name", '')
        sex_id = request.GET.get("sex_id", '')
        dent_id = request.GET.get("dent_id", '')

        search_field['name'] = name
        search_field['sex_id'] = sex_id
        search_field['dent_id'] = dent_id


        # GET 字段 篩選

        if sex_id and dent_id:
            user_obj = models.UserProfile.objects.filter(name__contains=name, sex=sex_id, dent_id=dent_id)
        elif sex_id:
            user_obj = models.UserProfile.objects.filter(name__contains=name, sex=sex_id)
        elif dent_id:
            user_obj = models.UserProfile.objects.filter(name__contains=name, dent_id=dent_id)
        else:
            user_obj = models.UserProfile.objects.filter(name__contains=name)

    # 分頁功能

    paginator = Paginator(user_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        user_obj = paginator.page(page)
    except PageNotAnInteger:
        user_obj = paginator.page(1)
    except EmptyPage:
        user_obj = paginator.page(paginator.num_pages)

    # 增
    if request.method == 'POST':

        print("This is POST")

        form_obj = forms.User_Add_Form(data=request.POST)

        fields = set(list(dict(form_obj.fields).keys()))
        errors = set(list(form_obj.errors.keys()))

        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)

        print(form_obj.errors)

        if form_obj.is_valid():

            # 取值
            name = form_obj.cleaned_data.get('name')
            sex = form_obj.cleaned_data.get('sex')
            code = form_obj.cleaned_data.get('code')
            dent = form_obj.cleaned_data.get('dent')
            username = form_obj.cleaned_data.get('username')

            # 創建user
            user = User()
            user.username = username
            user.set_password('12345678')
            user.is_staff = False
            user.save()

            # 創建Userinfo

            # 只取編號不包含部門編號
            code = code[len(dent.block_number):]
            models.UserProfile.objects.create(user=user, name=name, sex=sex, code=code, dent=dent)

            # result
            ret['status'] = 'ok'
            ret['msg'] = '新增成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        else:

            ret['status'] = 'error'
            ret['msg'] = '用戶信息輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        return JsonResponse(ret)

    # 改
    if request.method == 'PUT':
        return JsonResponse(ret)

    # 刪
    if request.method == 'DELETE':
        return JsonResponse(ret)

    return render(request, 'user/index.html', locals())


def userinfo(request, pk):
    # pk = 804

    userinfo_obj = models.UserProfile.objects.get(id=pk)

    if request.method == 'GET':
        forms_user_obj = forms.UserForm(instance=userinfo_obj.user,request=request)
        forms_userproinfo_obj = forms.UserProfileForm(instance=userinfo_obj,request=request)

    elif request.method == 'POST':

        print(request.POST)


        forms_user_obj = forms.UserForm(request.POST,instance=userinfo_obj.user,request=request)
        forms_userproinfo_obj = forms.UserProfileForm(request.POST,instance=userinfo_obj,request=request)


        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():
            print("ok")
        else:
            print("error")
            print(forms_user_obj.errors)
            print(forms_userproinfo_obj.errors)





    return render(request, "user/userinfo.html", locals())


def test1(request):
    print("this is test1")

    forms_obj = forms.test1Form()
    print(models.Catagory.objects.filter(id=2))
    print([models.Catagory.objects.get(id=2)])
    data = {'id': '', 'cary': models.Catagory.objects.filter(id=2), 'dent': models.Department.objects.filter(id=8)}
    print(data)
    forms_obj1 = forms.test1Form(data)

    # forms_obj1.fields["cary"].queryset=models.Catagory.objects.filter(id=2)
    # forms_obj1.fields["dent"].queryset=models.Department.objects.filter(id=8)

    print("forms_obj1.errors", forms_obj1.errors)

    if request.method == "POST":
        print(request.POST)

        print("forms_obj.errors",forms_obj.errors)

    return render(request, "test/test1.html", locals())


def test2(request):

    userinfo_obj = models.UserProfile.objects.get(id=796)
    # dent_obj = models.Department.objects.all()

    if request.method == 'GET':
        forms_user_obj = forms.UserForm(instance=userinfo_obj.user,request=request)
        forms_userproinfo_obj = forms.UserProfileForm(instance=userinfo_obj,request=request)

    elif request.method == 'POST':

        print(request.POST)


        forms_user_obj = forms.UserForm(request.POST,instance=userinfo_obj.user,request=request)
        forms_userproinfo_obj = forms.UserProfileForm(request.POST,instance=userinfo_obj,request=request)


        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():
            print("ok")
        else:
            print("error")

        print(forms_user_obj.errors)
        print(forms_userproinfo_obj.errors)



    return render(request, "test/test2.html", locals())