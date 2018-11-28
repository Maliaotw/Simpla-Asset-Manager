from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, FileResponse
from django.http import QueryDict
from asset import models
from asset import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
import pandas as pd
import re
import datetime
import csv
from django.http import StreamingHttpResponse


def file_iterator(file_name, chunk_size=512):
    f = open(file_name, encoding="utf8")
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break


# --- 資產 ---

def asset(request):
    # for asset in models.Asset.objects.all():
    #     print(asset)

    search_field = {}

    category_obj = models.Category.objects.all()
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
            asset_obj = models.Asset.objects.filter(name__contains=name, category_id=cate_id, department_id=dent_id)
        elif cate_id:
            asset_obj = models.Asset.objects.filter(name__contains=name, category_id=cate_id)
        elif dent_id:
            asset_obj = models.Asset.objects.filter(name__contains=name, department_id=dent_id)
        else:
            asset_obj = models.Asset.objects.filter(name__contains=name)

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
        forms_obj = forms.Asset_Add_Form(data=request.POST, request=request)

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
                data['category'] = models.Category.objects.filter(code=cate_code1)

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

            forms_obj = forms.Asset_Add_Form(data=data, request=request)

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
        print(request.POST)

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
        opts = models.Department.objects.all().model._meta

        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 分析
        data_ret = []

        df = pd.read_excel(file.name)
        print(df.head())

        def foo(x):
            print(x)
            if len(str(x)) < 3:
                return "%03d" % x
            else:
                return x

        df['部門負責人'] = df['部門負責人'].map(foo)


        # <class 'list'>: ['部門名稱', '部門簡稱', '部門工/代號', '部門工/代號碼長度', '部門負責人']
        verbose_names = [field.verbose_name for field in opts.fields]
        verbose_names.remove('ID')

        # <class 'list'>: ['id', 'name', 'code', 'block_number', 'block_number_len', 'user']
        field_names = [field.name for field in opts.fields]
        field_names.remove('id')

        # 要更改的 column name
        col_name = {v: f for f, v in zip(field_names, verbose_names)}
        col_cn_name = {f: v for f, v in zip(field_names, verbose_names)}

        df = df.rename(columns=col_name)
        # print(df.head())
        rows = df.to_dict("record")

        for row in rows:
            forms_obj = forms.Dent_Input_Form(data=row)

            if forms_obj.is_valid():
                data_ret.append(forms_obj)
            else:
                print(forms_obj.errors)
                for e in forms_obj.errors:  #
                    print(e, row[e])
                    ret['status'] = 'error'
                    ret['msg'] = '%s "%s"錯誤' % (col_cn_name[e], row[e])
                    data_ret = []
                    break

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            print("data_ret", data_ret)
            for form in data_ret:
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


def department_output(request):
    opts = models.Department.objects.all().model._meta

    file_name = "%E9%83%A8%E9%96%80.xlsx"

    # ['ID', '部門名稱', '部門簡稱', '部門工/代號', '部門工/代號碼長度', '部門負責人']
    row_names = [field.verbose_name for field in opts.fields]
    # print(row_names)

    # ['id', 'name', 'code', 'block_number', 'block_number_len', 'user']
    field_names = [field.name for field in opts.fields]
    # print(field_names)

    data = [{field.verbose_name: getattr(obj, field.name) for field in opts.fields} for obj in
            models.Department.objects.all()]
    # print(data)
    df = pd.DataFrame(data)
    df.to_excel(file_name)

    file = open(file_name, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/vnd.ms-excel;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="%s"' % file_name

    return response


# --- 類型 ---

def category(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    search_field = {}

    category_obj = models.Category.objects.all()

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

        cary_obj = models.Category.objects.get(id=cary_id)

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

        cary_obj = models.Category.objects.get(id=id)
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

        df = pd.read_excel(file.name)

        verbose_names = ['名稱', '代號']
        field_names = ['name', 'code']

        # 要更改的 column name
        col_name = {v: f for f, v in zip(field_names, verbose_names)}
        col_cn_name = {f:v for f, v in zip(field_names, verbose_names)}

        df = df.rename(columns=col_name)
        print(df.head())
        rows = df.to_dict("record")

        for row in rows:
            forms_obj = forms.CaryForm(data=row)

            if forms_obj.is_valid():
                data_ret.append(forms_obj)
            else:
                # print(forms_obj.errors)
                for e in forms_obj.errors: #
                    print(e, row[e])
                    ret['status'] = 'error'
                    ret['msg'] = '%s "%s"錯誤' % (col_cn_name[e],row[e])
                    data_ret = []
                    break

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            print("data_ret", data_ret)
            for form in data_ret:
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


def category_output(request):
    opts = models.Category.objects.all().model._meta
    print(request)

    file_name = "%E9%A1%9E%E5%9E%8B.xlsx"

    # ['ID', '名稱', '代號']
    row_names = [field.verbose_name for field in opts.fields]

    # ['id', 'name', 'code']
    field_names = [field.name for field in opts.fields]

    data = [{field.verbose_name: getattr(obj, field.name) for field in opts.fields} for obj in
            models.Category.objects.all()]

    print(data)
    df = pd.DataFrame(data)
    df.to_excel(file_name)

    file = open(file_name, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/vnd.ms-excel;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="%s"' % file_name

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
        forms_user_obj = forms.User_Add_Form()
        forms_userproinfo_obj = forms.UserProfile_Add_Form()

    if request.method == 'POST':

        forms_user_obj = forms.User_Add_Form(request.POST)
        forms_userproinfo_obj = forms.UserProfile_Add_Form(request.POST)

        fields = set(list(dict(forms_user_obj.fields).keys()) + list(dict(forms_userproinfo_obj.fields).keys()))
        errors = set(list(forms_user_obj.errors.keys()) + list(forms_userproinfo_obj.errors.keys()))

        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print("errors_fields", errors_fields)
        print("success_fields", success_fields)

        # 確認表單提交無誤

        print('forms_user_obj.is_valid()', forms_user_obj.is_valid())
        print('forms_userproinfo_obj.is_valid()', forms_userproinfo_obj.is_valid())

        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():

            # 創建User
            user_obj = forms_user_obj.save()
            data = forms_userproinfo_obj.cleaned_data
            data['user'] = user_obj
            models.UserProfile.objects.create(**data)

            print("ok")
            ret['status'] = 'ok'
            ret['msg'] = '新增成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields



        else:
            print("error")
            print(forms_user_obj.errors)
            print(forms_userproinfo_obj.errors)

            ret['status'] = 'error'
            ret['msg'] = '用戶信息輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        return JsonResponse(ret)

    return render(request, "user/user_add.html", locals())


def user_edit(request, pk):
    ret = {"status": "", "re_html": "", "msg": ""}

    userinfo_obj = models.UserProfile.objects.get(id=pk)

    print("request.method", request.method)

    if request.method == 'GET':
        forms_user_obj = forms.User_Edit_Form(instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfile_Edit_Form(instance=userinfo_obj, request=request)

    elif request.method == 'POST':

        print("request.POST", request.POST)

        forms_user_obj = forms.User_Edit_Form(request.POST, instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfile_Edit_Form(request.POST, instance=userinfo_obj, request=request)

        fields = set(list(dict(forms_user_obj.fields).keys()) + list(dict(forms_userproinfo_obj.fields).keys()))
        errors = set(list(forms_user_obj.errors.keys()) + list(forms_userproinfo_obj.errors.keys()))

        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)

        # 確認表單提交無誤
        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():
            # 把判斷都交給Form表單並儲存
            forms_user_obj.save()
            forms_userproinfo_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '修改成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        else:

            ret['status'] = 'error'
            ret['msg'] = '用戶信息輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        return JsonResponse(ret)

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
    print(models.Category.objects.filter(id=2))
    print([models.Category.objects.get(id=2)])
    data = {'id': '', 'cary': models.Category.objects.filter(id=2), 'dent': models.Department.objects.filter(id=8)}
    print(data)
    forms_obj1 = forms.test1Form(data)

    # forms_obj1.fields["cary"].queryset=models.Category.objects.filter(id=2)
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
