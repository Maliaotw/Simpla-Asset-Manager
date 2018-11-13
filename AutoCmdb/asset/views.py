from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, FileResponse
from django.http import QueryDict
from asset import models
from asset import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
import pandas as pd
import csv
import re
import datetime
import csv


# --- 資產 ---

def asset(request):

    # for asset in models.Asset.objects.all():
    #     print(asset)

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


def asset_add(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':
        forms_obj = forms.Asset_Add_Form(request=request)


    elif request.method == 'POST':

        print(request.POST)
        forms_obj = forms.Asset_Add_Form(request.POST, request=request)

        print(forms_obj.errors)
        #
        fields = set(list(dict(forms_obj.fields).keys()))
        errors = set(list(forms_obj.errors.keys()))
        #
        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)
        #

        if forms_obj.is_valid():
            print("ok")
            ret['status'] = 'ok'
            ret['msg'] = '新增成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

            forms_obj.save()

        else:
            print("error")
            ret['status'] = 'error'
            ret['msg'] = '輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

            print(forms_obj.errors)

        return JsonResponse(ret)

    return render(request, "asset/asset_add.html", locals())


def asset_edit(request, pk):
    ret = {"status": "", "re_html": "", "msg": ""}

    asset_obj = models.Asset.objects.get(id=pk)

    if request.method == 'GET':
        forms_obj = forms.Asset_Edit_Form(instance=asset_obj, request=request)

    if request.method == 'POST':

        forms_obj = forms.Asset_Edit_Form(data=request.POST, instance=asset_obj, request=request)

        print(forms_obj.errors)

        fields = set(list(dict(forms_obj.fields).keys()))
        errors = set(list(forms_obj.errors.keys()))

        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)

        if forms_obj.is_valid():
            print("ok")
            ret['status'] = 'ok'
            ret['msg'] = '修改成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields
            forms_obj.save()
        else:
            print("error")
            ret['status'] = 'error'
            ret['msg'] = '輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        return JsonResponse(ret)

    return render(request, "asset/asset_edit.html", locals())


def asset_input(request):
    ret = {'status': '', "msg": ''}

    if request.method == 'GET':
        return render(request, "asset/input.html", locals())

    if request.method == 'POST':

        # 存取檔案
        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 分析
        data_ret = []

        f = open(file.name, 'r')
        print(csv.DictReader(f).line_num)
        rows = csv.DictReader(f)
        for row in rows:

            verbose_name = ['資產編號', '價格', '類型', '部門', '負責人', '購買日期', '狀態']
            field_name = ['sn', 'price', 'category', 'department', 'manager', 'purchase_date', 'status']

            keys = {k: name for k, name in zip(field_name, verbose_name)}
            data = {k: row[name] for k, name in zip(field_name, verbose_name)}

            # PC-066
            cate_code1, data['sn'] = data['sn'].split("-")

            # 找到類型對象
            cate_name, cate_code2 = data['category'].replace(")", "").split("(")
            if cate_code1 == cate_code2:
                data['category'] = models.Catagory.objects.filter(code=cate_code1)

            # 找到部門對象
            if data['department']:
                dent_name, dent_code = data['department'].replace(")", "").split("(")
                data['department'] = models.Department.objects.filter(code=dent_code)


            # 找到負責人 對象
            if data['manager']:
                manager_name, manager_code = data['manager'].replace(")", "").split("(")
                data['manager'] = models.UserProfile.objects.filter(name=manager_name)

            # 購買日期
            data['purchase_date'] = datetime.datetime.strptime(data['purchase_date'], '%Y/%m/%d')

            forms_obj = forms.Asset_Add_Form(data=data,request=request)

            if forms_obj.is_valid():
                data_ret.append(forms_obj)

            else:
                print(forms_obj.errors)
                for e in forms_obj.errors:
                    print(e, data[e], keys[e])
                    ret['status'] = 'error'
                    ret['msg'] = '%s"%s"錯誤' % (keys[e], data[e])
                    data_ret = []
                    break

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            print("data_ret", data_ret)
            for form in data_ret:
                # print(form)
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


def asset_output(request):
    opts = models.Asset.objects.all().model._meta
    response = HttpResponse(content_type='text/csv; charset=cp936')

    # force download.
    response['Content-Disposition'] = 'attachment;filename=asset.csv'
    # the csv writer
    writer = csv.writer(response)

    # ['ID', '資產編號', '價格', '類型', '部門', '負責人', '購買日期', '狀態', '更新日期', '創建日期']
    row_names = [field.verbose_name for field in opts.fields]
    print(row_names)

    # ['id', 'sn', 'price', 'category', 'department', 'manager', 'purchase_date', 'status', 'latest_date', 'create_date']
    field_names = [field.name for field in opts.fields]
    print(field_names)

    # Write a first row with header information
    writer.writerow(row_names)
    # Write data rows
    for obj in models.Asset.objects.all():
        ret = []
        ret.append(obj.id)
        sn = "%s-%s" % (obj.category.code, obj.sn)
        ret.append(sn)
        ret.append(obj.price)
        ret.append(obj.category)
        ret.append(obj.department)
        ret.append(obj.manager)
        ret.append(obj.purchase_date.strftime("%Y/%m/%d") if obj.purchase_date else "")
        ret.append(obj.get_status_display())
        ret.append(obj.latest_date.strftime("%Y/%m/%d") if obj.latest_date else "")
        ret.append(obj.create_date.strftime("%Y/%m/%d") if obj.create_date else "")
        writer.writerow(ret)

    return response


# --- 部門 ---

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

    return render(request, "department/index.html", locals())


def department_input(request):
    ret = {'status': '', "msg": ''}

    if request.method == 'GET':
        return render(request, "department/input.html", locals())

    if request.method == 'POST':
        # 存取檔案
        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 分析
        data_ret = []

        f = open(file.name, 'r')
        print(csv.DictReader(f).line_num)
        rows = csv.DictReader(f)
        for row in rows:
            verbose_name = ['部門名稱', '部門簡稱', '部門工/代號', '部門工/代號碼長度', '部門負責人']
            field_name = ['name', 'code', 'block_number', 'block_number_len', 'user']

            keys = {k: name for k, name in zip(field_name, verbose_name)}
            data = {k: row[name] for k, name in zip(field_name, verbose_name)}

            # 找到負責人 對象
            if data['user']:
                manager_name, manager_code = data['user'].replace(")", "").split("(")
                data['user'] = models.UserProfile.objects.filter(name=manager_name)


            forms_obj = forms.DentForm(data=data)

            if forms_obj.is_valid():
                data_ret.append(forms_obj)

            else:
                print(forms_obj.errors)
                for e in forms_obj.errors:
                    print(e, data[e], keys[e])
                    ret['status'] = 'error'
                    ret['msg'] = '%s"%s"錯誤' % (keys[e], data[e])
                    data_ret = []
                    break

            # 匯入
        if ret['status'] == 'error':
            pass
        else:
            print("data_ret", data_ret)
            for form in data_ret:
                # print(form)
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

            # 必須傳回JSON
        return JsonResponse(ret)


def department_output(request):
    opts = models.Department.objects.all().model._meta
    response = HttpResponse(content_type='text/csv; charset=cp936')

    # force download.
    response['Content-Disposition'] = 'attachment;filename=department.csv'
    # the csv writer
    writer = csv.writer(response)

    # ['ID', '部門名稱', '部門簡稱', '部門工/代號', '部門工/代號碼長度', '部門負責人']
    row_names = [field.verbose_name for field in opts.fields]
    # print(row_names)

    # ['id', 'name', 'code', 'block_number', 'block_number_len', 'user']
    field_names = [field.name for field in opts.fields]
    # print(field_names)

    # Write a first row with header information
    writer.writerow(row_names)

    ret = [writer.writerow([getattr(obj,field) for field in field_names]) for obj in models.Department.objects.all()]

    return response


# --- 類型 ---

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

    return render(request, "category/index.html", locals())


def category_input(request):
    ret = {'status': '', "msg": ''}

    if request.method == 'GET':
        return render(request, "category/input.html", locals())

    if request.method == 'POST':
        # 存取檔案
        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 分析
        data_ret = []

        f = open(file.name, 'r')
        print(csv.DictReader(f).line_num)
        rows = csv.DictReader(f)
        for row in rows:
            verbose_name = ['名稱', '代號']
            field_name = ['name', 'code']

            keys = {k: name for k, name in zip(field_name, verbose_name)}
            data = {k: row[name] for k, name in zip(field_name, verbose_name)}


            forms_obj = forms.CaryForm(data=data)

            if forms_obj.is_valid():
                data_ret.append(forms_obj)

            else:
                print(forms_obj.errors)
                for e in forms_obj.errors:
                    print(e, data[e], keys[e])
                    ret['status'] = 'error'
                    ret['msg'] = '%s"%s"錯誤' % (keys[e], data[e])
                    data_ret = []
                    break

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            print("data_ret", data_ret)
            for form in data_ret:
                # print(form)
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


def category_output(request):
    opts = models.Catagory.objects.all().model._meta
    response = HttpResponse(content_type='text/csv; charset=cp936')

    # force download.
    response['Content-Disposition'] = 'attachment;filename=Catagory.csv'
    # the csv writer
    writer = csv.writer(response)

    # ['ID', '名稱', '代號']
    row_names = [field.verbose_name for field in opts.fields]
    print(row_names)

    # ['id', 'name', 'code']
    field_names = [field.name for field in opts.fields]
    print(field_names)

    # Write a first row with header information
    writer.writerow(row_names)

    ret = [writer.writerow([getattr(obj, field) for field in field_names]) for obj in models.Catagory.objects.all()]

    return response


# --- 用戶 ---

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
        sex = request.GET.get("sex", '')
        dent_id = request.GET.get("dent_id", '')

        search_field['name'] = name
        search_field['sex'] = sex
        search_field['dent_id'] = dent_id

        # GET 字段 篩選

        if sex and dent_id:
            user_obj = models.UserProfile.objects.filter(name__contains=name, sex=sex, dent_id=dent_id)
        elif sex:
            user_obj = models.UserProfile.objects.filter(name__contains=name, sex=sex)
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

        # 驗證錯誤及正常字段
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


def user_info(request):
    pass


def user_add(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':
        forms_obj = forms.User_Add_Form()

    if request.method == 'POST':

        print("This is POST")

        form_obj = forms.User_Add_Form(data=request.POST)
        print(request.POST)

        print(form_obj.errors)
        #
        fields = set(list(dict(form_obj.fields).keys()))
        errors = set(list(form_obj.errors.keys()))
        #
        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)
        #
        print(form_obj.errors)
        #
        if form_obj.is_valid():
            print("ok")

            form_obj.save()

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

    return render(request, "user/user_add.html", locals())


def user_edit(request, pk):
    # pk = 804

    userinfo_obj = models.UserProfile.objects.get(id=pk)

    if request.method == 'GET':
        forms_user_obj = forms.UserForm(instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(instance=userinfo_obj, request=request)

    if request.method == 'POST':

        print(request.POST)

        forms_user_obj = forms.UserForm(request.POST, instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(request.POST, instance=userinfo_obj, request=request)

        # 確認表單提交無誤
        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():
            print("ok")

            # 取值

            username = forms_user_obj.cleaned_data.get('username')
            is_staff = forms_user_obj.cleaned_data.get('is_staff')

            password1 = forms_user_obj.cleaned_data.get('password1')
            password2 = forms_user_obj.cleaned_data.get('password2')

            name = forms_userproinfo_obj.cleaned_data.get('name')
            in_service = forms_userproinfo_obj.cleaned_data.get('in_service')
            birthday = forms_userproinfo_obj.cleaned_data.get('birthday')
            sex = forms_userproinfo_obj.cleaned_data.get('sex')
            code = forms_userproinfo_obj.cleaned_data.get('code')
            dent = forms_userproinfo_obj.cleaned_data.get('dent')

            userinfo = forms_user_obj.save(commit=False)
            # 修改密碼
            if password1 and password2:
                userinfo.user.set_password(password1)

            # 修改用戶

            userinfo.save()

            # 修改用戶profifle
            code = code[len(dent.block_number):]

            userproinfo_obj = forms_userproinfo_obj.save(commit=False)
            userproinfo_obj.code = code
            userproinfo_obj.save()


        else:
            print("error")
            print(forms_user_obj.errors)
            print(forms_userproinfo_obj.errors)

    return render(request, "user/user_edit.html", locals())


def user_input(request):
    ret = {'status': '', "msg": ''}

    if request.method == 'GET':
        return render(request, "user/input.html", locals())

    if request.method == 'POST':

        # 存取檔案
        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 分析
        data_ret = []

        f = open(file.name, 'r')
        print(csv.DictReader(f).line_num)
        rows = csv.DictReader(f)
        for row in rows:

            verbose_name = ['用户名', '姓名', '員工編號', '性別', '部門', '在職狀態', '生日日期', '登入']
            field_name = ['username', 'name', 'code', 'sex', 'dent', 'in_service', 'birthday', 'is_staff']

            keys = {k: name for k, name in zip(field_name, verbose_name)}
            data = {k: row[name] for k, name in zip(field_name, verbose_name)}

            data['dent'] = models.Department.objects.filter(name=data['dent'])
            data['birthday'] = datetime.datetime.strptime(data['birthday'], '%Y/%m/%d')

            is_staff_coice = {'是': True, '否': False}
            if data['is_staff'] in list(is_staff_coice.keys()):
                data['is_staff'] = is_staff_coice[data['is_staff']]

            forms_obj = forms.User_Add_Form(data=data)

            if forms_obj.is_valid():
                data_ret.append(forms_obj)

            else:
                print(forms_obj.errors)
                for e in forms_obj.errors:
                    print(e, data[e], keys[e])
                    ret['status'] = 'error'
                    ret['msg'] = '%s"%s"錯誤' % (keys[e], data[e])
                    data_ret = []
                    break

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            print("data_ret", data_ret)
            for form in data_ret:
                # print(form)
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


def user_output(request):
    opts = models.UserProfile.objects.all().model._meta
    response = HttpResponse(content_type='text/csv; charset=cp936')

    # force download.
    response['Content-Disposition'] = 'attachment;filename=user.csv'
    # the csv writer
    writer = csv.writer(response)

    # ID user 姓名 員工編號 性別 部門 在職狀態 生日日期
    row_names = [field.verbose_name for field in opts.fields]
    print(row_names)

    # ['id', 'sn', 'price', 'category', 'department', 'manager', 'purchase_date', 'status', 'latest_date', 'create_date']
    field_names = [field.name for field in opts.fields]
    print(field_names)

    # Write a first row with header information
    writer.writerow(row_names)
    # Write data rows
    for obj in models.UserProfile.objects.all():
        ret = []
        ret.append(obj.id)
        ret.append(obj.user.username)
        ret.append(obj.name)
        ret.append(str("{}{}".format(obj.dent.block_number, obj.code)))
        ret.append(obj.sex)
        ret.append(obj.dent.name)
        ret.append(obj.in_service)
        ret.append(obj.birthday.strftime("%Y/%m/%d") if obj.birthday else "")
        writer.writerow(ret)

    return response


# --- 測試 ---

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

        print("forms_obj.errors", forms_obj.errors)

    return render(request, "test/test1.html", locals())


def test2(request):
    userinfo_obj = models.UserProfile.objects.get(id=796)
    # dent_obj = models.Department.objects.all()

    if request.method == 'GET':
        forms_user_obj = forms.UserForm(instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(instance=userinfo_obj, request=request)

    elif request.method == 'POST':

        print(request.POST)

        forms_user_obj = forms.UserForm(request.POST, instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(request.POST, instance=userinfo_obj, request=request)

        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():
            print("ok")
        else:
            print("error")

        print(forms_user_obj.errors)
        print(forms_userproinfo_obj.errors)

    return render(request, "test/test2.html", locals())
