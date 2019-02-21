from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, FileResponse, HttpResponseRedirect, StreamingHttpResponse, QueryDict
from asset import models, forms, roles
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
import datetime
import csv
import numpy as np
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings


# --- 資產 ---


@login_required
def asset(request):
    '''
    暫定首頁
    :param request:
    :return:
    '''
    print('Assset')

    # 驗證用戶
    # news_obj = models.News.objects.filter(userprofile__in=request.user.userprofile)

    # print(news_obj)

    admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
    if request.user.userprofile.dent in admindent:
        print('管理用戶')
        # category_obj = models.Category.objects.all()
        asset_obj = models.Asset.objects.all()
        asset_repair_obj = models.AssetRepair.objects.filter(status=False)
        news_obj = models.News.objects.exclude(userprofile__user_id=request.user.id)
        # user_obj = models.UserProfile.objects.all()

    else:
        # print('一般用戶')
        # search_field['dent_id'] = dent_id
        # dent_id = request.user.userprofile.dent_id
        news_obj = models.News.objects.filter(dent=request.user.userprofile.dent).all()
        news_obj = news_obj.exclude(userprofile__user_id=request.user.id)
        asset_obj = models.Asset.objects.filter(department=request.user.userprofile.dent)
        asset_repair_obj = models.AssetRepair.objects.filter(asset_obj__in=asset_obj, status=False)

    return render(request, "asset/home.html", locals())


@login_required
@permission_required('asset.can_view_asset')
def asset_index(request):
    print('Asset_index')
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == "GET":

        search_field = {}
        # contacts = 10

        # GET 字段
        name = request.GET.get("name", '')
        cate_id = request.GET.get("cate_id", '')
        dent_id = request.GET.get("dent_id", '')
        contacts = request.GET.get('contacts', 10)

        # print(request.user)
        category_obj = models.Category.objects.all()

        # 驗證用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        if request.user.userprofile.dent in admindent:
            print('管理用戶')
            # category_obj = models.Category.objects.all()
            department_obj = models.Department.objects.all()
            # user_obj = models.UserProfile.objects.all()
            search_field['name'] = name
            search_field['cate_id'] = cate_id
            search_field['dent_id'] = dent_id
        else:
            # print('一般用戶')
            search_field['name'] = name
            search_field['cate_id'] = cate_id
            # search_field['dent_id'] = dent_id
            dent_id = request.user.userprofile.dent_id
            search_field['dent_id'] = dent_id

        # print(search_field)

        # GET 字段 篩選
        if cate_id and dent_id:
            # asset_repair_obj = asset_repair_obj.filter(
            #   Q(asset_obj__name__contains=name) | Q(title__contains=name)
            # )
            asset_obj = models.Asset.objects.filter(
                Q(
                    name__contains=name, category_id=cate_id, department_id=dent_id
                ) | Q(
                    manager__code__contains=name, category_id=cate_id, department_id=dent_id
                )
            )
        elif cate_id:
            asset_obj = models.Asset.objects.filter(
                Q(name__contains=name, category_id=cate_id) | Q(manager__code__contains=name, category_id=cate_id)
            )
        elif dent_id:
            asset_obj = models.Asset.objects.filter(
                Q(name__contains=name, department_id=dent_id) | Q(manager__code__contains=name, department_id=dent_id)
            )
        elif name:
            asset_obj = models.Asset.objects.filter(
                Q(name__contains=name) | Q(manager__code__contains=name)
            )
        else:
            asset_obj = models.Asset.objects.all()

        # print('asset_obj', asset_obj)
        # 分頁功能

        search_field['contacts'] = contacts
        paginator = Paginator(asset_obj, contacts)  # Show 10 contacts per page

        page = request.GET.get('page', 1)
        try:
            asset_obj = paginator.page(page)
        except PageNotAnInteger:
            asset_obj = paginator.page(1)
        except EmptyPage:
            asset_obj = paginator.page(paginator.num_pages)

        # print('asset_obj',asset_obj)

        return render(request, "asset/index.html", locals())

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

    if request.method == 'DELETE':
        print("THIS IS DELETE")
        put = QueryDict(request.body)
        print(put)
        id = put.get('id')
        news_obj = models.Asset.objects.get(id=id)
        news_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)





@login_required
@permission_required('asset.can_view_asset')
def asset_add(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':
        forms_obj = forms.Asset_Add_Form(request=request)


    elif request.method == 'POST':

        print(request.POST)
        forms_obj = forms.Asset_Add_Form(data=request.POST, request=request)

        # print(forms_obj.errors)
        #
        fields = set(list(dict(forms_obj.fields).keys()))
        errors = set(list(forms_obj.errors.keys()))
        #
        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        # print(errors_fields)
        # print(success_fields)
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


@login_required
@permission_required('asset.can_view_asset')
def asset_edit(request, pk):
    ret = {"status": "", "re_html": "", "msg": ""}

    asset_obj = models.Asset.objects.get(id=pk)

    if request.method == 'GET':
        forms_obj = forms.Asset_Edit_Form(instance=asset_obj, request=request)

        asset_record_obj = models.AssetRecord.objects.filter(asset_obj=asset_obj)
        # print(asset_record_obj)
        asset_repair_obj = models.AssetRepair.objects.filter(asset_obj=asset_obj)

        # 關聯資產
        relation_assets_obj = models.AssetToAssets.objects.filter(asset_obj=asset_obj)
        # print(relation_assets_obj)

        # 資產關聯資產表單
        category_obj = models.Category.objects.all()
        user_dent = request.user.userprofile.dent

        # 驗證用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        if request.user.userprofile.dent in admindent:
            data = {
                cate.id: list(
                    models.Asset.objects.filter(category=cate).values('id', 'name')
                ) for cate in category_obj
            }
        else:
            data = {
                cate.id: list(
                    models.Asset.objects.filter(category=cate, department=user_dent).values('id', 'name')
                ) for cate in category_obj
            }
        # print(data)

        # 被關聯資產
        on_rel_assets_obj = models.AssetToAssets.objects.filter(assets=asset_obj)
        print(on_rel_assets_obj)

        ata_forms_obj = forms.AssetToAssetsForm(request=request)

        return render(request, "asset/asset_edit.html", locals())

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


@login_required
@permission_required('asset.can_view_asset')
def asset_input(request):
    ret = {'status': '', "msg": '', 'errordict': {}}

    if request.method == 'GET':
        return render(request, "asset/input.html", locals())

    if request.method == 'POST':
        opts = models.Asset.objects.all().model._meta

        # 存取檔案
        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 分析
        data_ret = []

        # 讀取excel
        df = pd.read_excel(file.name)

        # <class 'list'>:['ID', '資產編號', '資產號碼', '價格', '類型', '部門', '負責人', '購買日期', '狀態', '更新日期', '創建日期']
        verbose_names = [field.verbose_name for field in opts.fields]
        # print(verbose_names)
        verbose_names.remove('ID')

        # <class 'list'>: ['id', 'name', 'number', 'price', 'category', 'department', 'manager', 'purchase_date', 'status', 'latest_date', 'create_date']
        field_names = [field.name for field in opts.fields]
        # print(field_names)
        field_names.remove('id')

        # 更改 column name
        col_name = {v: f for f, v in zip(field_names, verbose_names)}
        col_cn_name = {f: v for f, v in zip(field_names, verbose_names)}
        df = df.rename(columns=col_name)

        # 將nan 轉為 '' 字符串
        df = df.astype(object).replace(np.nan, '')

        rows = df.to_dict("record")
        # print(rows)

        for i, row in enumerate(rows):
            # print('row', row)

            forms_obj = forms.Asset_Input_Form(data=row, request=request)
            if forms_obj.is_valid():
                data_ret.append(forms_obj)
            else:
                # print(forms_obj.errors)
                # print(dir(forms_obj.errors))
                print(forms_obj.errors.as_json())
                error = {i + 1: []}
                for k, v in forms_obj.errors.items():
                    # print(k, col_cn_name[k], row[k])
                    # print(v)
                    ret['status'] = 'error'
                    data = {'name': col_cn_name[k], 'message': v[0], 'content': row[k]}
                    error[i + 1].append(data)
                    # ret['msg'] += '%s "%s"錯誤' % (col_cn_name[e], row[e])
                    # data_ret = []
                ret['errordict'].update(error)

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            # print("data_ret", data_ret)
            for form in data_ret:
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


@login_required
@permission_required('asset.can_view_asset')
def asset_output(request):
    opts = models.Asset.objects.all().model._meta

    file_name = r'demo_files/資產/DEMO_資產.xlsx'
    output_name = "%E8%B3%87%E7%94%A2.xlsx"

    # ['ID', '資產編號', '資產號碼', '價格', '類型', '部門', '負責人', '購買日期', '狀態', '更新日期', '創建日期']
    # row_names = [field.verbose_name for field in opts.fields]
    # print(row_names)

    # ['id', 'name', 'number', 'price', 'category', 'department', 'manager', 'purchase_date', 'status', 'latest_date', 'create_date']
    # fields = [field.name for field in opts.fields]
    # print(fields)

    data = [{field.verbose_name: getattr(obj, field.name) for field in opts.fields} for obj in
            models.Asset.objects.all()]

    df = pd.DataFrame(data)

    # 刪除欄位
    df = df.drop('ID', axis=1)
    df = df.drop('更新日期', axis=1)
    df = df.drop('創建日期', axis=1)
    df = df.drop('資產號碼', axis=1)

    df.to_excel(file_name)

    file = open(file_name, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/vnd.ms-excel;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="%s"' % output_name

    return response


@login_required
def asset_busunit(request):
    '''
    資產業務線表
    :param request:
    :return:
    '''

    if request.method == 'GET':
        search_field = {}

        # GET 字段
        name = request.GET.get("name", '')
        cate_id = request.GET.get("cate_id", '')
        dent_id = request.GET.get("dent_id", '')
        busunit_id = request.GET.get("busunit_id", '')
        contacts = request.GET.get('contacts', 10)

        # asset_busunit_obj = models.AssetBusiness.objects.all()
        category_obj = models.Category.objects.all()
        department_obj = models.Department.objects.all()

        # 判斷管理用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        # admindent = models.Department.objects.filter(asset=

        if request.user.userprofile.dent in admindent:
            # print('管理用戶')
            asset_obj = models.Asset.objects.all()
            busunit_obj = models.BusinessUnit.objects.all()

        else:
            # print('一般用戶')
            asset_obj = models.Asset.objects.filter(department=request.user.userprofile.dent)
            busunit_obj = models.BusinessUnit.objects.filter(dent=request.user.userprofile.dent)

        get = {
            'cate_id': {
                "category_id": cate_id
            },
            'dent_id': {
                "department_id": dent_id
            },
            'busunit_id': {
                "assetbusiness__business_id": busunit_id
            }
        }
        if request.GET:

            data = request.GET.copy()

            for i in ['name', 'page', 'contacts']:
                if i in data:
                    data.pop(i)

            search_key = list(filter(lambda x: data[x] != "", data.keys()))
            # print(search_key)

            search_dict = {}
            for key in search_key:
                search_dict.update(get[key])
            # print(search_dict)

            asset_obj = asset_obj.filter(
                Q(name__contains=name), **search_dict
            )

        page = request.GET.get('page', 1)
        search_field['contacts'] = contacts
        paginator = Paginator(asset_obj, contacts)  # Show 10 contacts per page

        try:
            asset_obj = paginator.page(page)
        except PageNotAnInteger:
            asset_obj = paginator.page(1)
        except EmptyPage:
            asset_obj = paginator.page(paginator.num_pages)

        return render(request, 'asset/busunit.html', locals())

    if request.method == 'POST':
        print("POST")
        ret = {"status": "", "re_html": "", "msg": ""}

        # print(request.POST)
        assetid = request.POST.get("assetid")  # 資產ID
        ab_id = request.POST.get("ab_id")  # 資產業務線對應表ID
        busunitid = request.POST.get("busunitid")  # 業務線ID
        # print(assetid)
        # print(busunitid)

        asset_obj = models.Asset.objects.get(id=assetid)
        # print("bsnis_obj")
        if ab_id:
            ab_obj = models.AssetBusiness.objects.get(id=ab_id)
            ab_obj.asset = asset_obj
            if busunitid:
                bsnis_obj = models.BusinessUnit.objects.get(id=busunitid)
                ab_obj.business = bsnis_obj
            else:
                ab_obj.business = None

        else:
            if busunitid:
                bsnis_obj = models.BusinessUnit.objects.get(id=busunitid)
                ab_obj = models.AssetBusiness(asset=asset_obj, business=bsnis_obj)
        # print(ab_obj)
        ab_obj.save()
        ret['status'] = 'ok'

        return JsonResponse(ret)


# 資產關聯資產
@login_required
def ara(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'POST':

        print(request.POST)
        id = request.POST.get("asset_obj")
        form_obj = forms.AssetToAssetsForm(data=request.POST, request=request)

        if form_obj.is_valid():
            print("ok")
            form_obj.save()
            ret['status'] = 'ok'
            ret['msg'] = '新增成功'
            # return "%s%s" % (redirect("asset_edit"),'#tab_assets')
            # print("redirect('asset_edit', pk=id)",redirect('asset_edit', pk=id))
            # url = redirect('asset_edit', pk=id)
            # return redirect("%s#tab_assets" % url)
            return JsonResponse(ret)

    if request.method == 'PUT':
        put = QueryDict(request.body)
        print("put", put)
        id = put.get('id')

        ara_obj = models.AssetToAssets.objects.get(id=id)
        froms_obj = forms.AssetToAssetsForm(request=request, data=put, instance=ara_obj)
        print(froms_obj.errors)
        if froms_obj.is_valid():
            print("ok")
            froms_obj.save()
            ret['status'] = 'ok'
            ret['msg'] = '修改成功'

        return JsonResponse(ret)

    if request.method == 'DELETE':
        print("THIS IS DELETE")
        put = QueryDict(request.body)
        print(put)
        id = put.get('id')
        ara_obj = models.AssetToAssets.objects.get(id=id)
        ara_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)


# --- 業務線 ---

@login_required
def busunit(request):
    '''
    業務線列表
    :param request:
    :return:
    '''
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':

        search_field = {}

        dent_obj = models.Department.objects.all()

        # 判斷管理用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        # admindent = models.Department.objects.filter(asset=

        if request.user.userprofile.dent in admindent:
            # print('管理用戶')
            busunit_obj = models.BusinessUnit.objects.all()
        else:
            # print('一般用戶')
            busunit_obj = models.BusinessUnit.objects.filter(dent=request.user.userprofile.dent)

        paginator = Paginator(busunit_obj, 10)  # Show 10 contacts per page

        page = request.GET.get('page')
        try:
            busunit_obj = paginator.page(page)
        except PageNotAnInteger:
            busunit_obj = paginator.page(1)
        except EmptyPage:
            busunit_obj = paginator.page(paginator.num_pages)

        return render(request, 'busunit/index.html', locals())

    if request.method == 'POST':

        form_obj = forms.BusunitForm(data=request.POST)
        print(request.POST)

        if form_obj.is_valid():
            form_obj.save()
            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            print(form_obj.errors)
            ret['status'] = 'error'
            ret['msg'] = '新增信息輸入不正確!'

        return JsonResponse(ret)

    if request.method == 'PUT':
        print("THIS IS PUT")

        put = QueryDict(request.body)
        print(put)

        id = put.get('id')
        name = put.get('name')
        en = put.get('en')

        busunit_obj = models.BusinessUnit.objects.get(id=id)
        busunit_obj.name = name
        busunit_obj.en = en
        busunit_obj.save()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)

    if request.method == "DELETE":
        print("THIS IS DELETE")
        put = QueryDict(request.body)
        print(put)
        id = put.get('id')
        dent_obj = models.BusinessUnit.objects.get(id=id)
        dent_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)


# --- 資產維修紀錄 ---

@login_required
@permission_required('asset.can_view_asset')
def asset_repair(request):
    if request.method == 'GET':

        search_field = {}

        # Get字段
        name = request.GET.get("name", '')
        status = request.GET.get("status", '')
        contacts = request.GET.get('contacts', 10)

        # 判斷管理用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        # admindent = models.Department.objects.filter(asset=

        if request.user.userprofile.dent in admindent:
            # print('管理用戶')
            asset_repair_obj = models.AssetRepair.objects.all()
            # asset_repair_obj = models.AssetRepair.objects.filter(=)

        else:
            # print('一般用戶')
            # search_field['dent_id'] = dent_id
            # dent_id = request.user.userprofile.dent_id
            asset_repair_obj = models.AssetRepair.objects.filter(
                asset_obj__department=request.user.userprofile.dent)

        # 篩選
        # if status

        status_choices = (False, True)

        print('name', name)

        if status:
            asset_repair_obj = asset_repair_obj.filter(Q(asset_obj__name__contains=name) | Q(title__contains=name),
                                                       status=status_choices[int(status)])

        elif name:
            asset_repair_obj = asset_repair_obj.filter(Q(asset_obj__name__contains=name) | Q(title__contains=name))
        else:
            pass
        #     Question.objects.filter(Q(question_text_Q_contains='you') | Q(question_text__contains='who'))
        search_field['contacts'] = contacts
        paginator = Paginator(asset_repair_obj, contacts)  # Show 10 contacts per page

        page = request.GET.get('page', 1)

        try:
            asset_repair_obj = paginator.page(page)
        except PageNotAnInteger:
            asset_repair_obj = paginator.page(1)
        except EmptyPage:
            asset_repair_obj = paginator.page(paginator.num_pages)

        return render(request, 'asset_repair/index.html', locals())

    if request.method == 'DELETE':
        ret = {'status': '', 'code': '', 'msg': '', 'data': ''}

        print("DELETE")
        put = QueryDict(request.body)

        print(put)

        user = put.get('user')
        id = put.get('id')

        user = models.UserProfile.objects.get(id=user)

        if request.user.userprofile == user:
            asset_repair_obj = models.AssetRepair.objects.get(id=id)
            asset_repair_obj.delete()

            ret['msg'] = '成功'
            ret['status'] = 'ok'
            ret['code'] = 200

        return JsonResponse(ret)


@login_required
@permission_required('asset.can_view_asset')
def asset_repair_add(request):
    '''
    新增維修表單

    :param request:
    :return:
    '''
    if request.method == 'GET':
        forms_obj = forms.AssetRepair_ADD_Form(request=request)

        category = models.Category.objects.all()
        user_dent = request.user.userprofile.dent

        # 驗證用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        if request.user.userprofile.dent in admindent:
            data = {
                cate.id: list(
                    models.Asset.objects.filter(category=cate).values('id', 'name')
                ) for cate in category
            }
        else:
            data = {
                cate.id: list(
                    models.Asset.objects.filter(category=cate, department=user_dent).values('id', 'name')
                ) for cate in category
            }
        # print(data)

        return render(request, 'asset_repair/add.html', locals())

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        form = forms.AssetRepair_ADD_Form(request=request, data=request.POST)

        # m = models.AssetRepair()
        # m.photo.obj
        print(form.errors)

        if form.is_valid():
            obj = form.save()
            obj.creator = request.user.userprofile
            print(form.cleaned_data['photo'])

            # obj.photo.add(form.cleaned_data['photo'])
            for i in form.cleaned_data['photo']:
                obj.photo.add(i)

            obj.save()

        return redirect('/asset/repair')


@csrf_exempt
def asset_file(request):
    '''
    上傳資產紀錄附件檔案
    :param request:
    :return:
    '''
    if request.method == 'POST':
        print(request)
        print('POST' * 10)

        name = request.FILES['img'].name

        print(name)

        i = models.AssetRepairImage(name=name, photo=request.FILES['img'])
        i.save()

        # print(i.save())
        # print(dir(i))
        # print(dir(i.photo))
        # print(i)
        # print(i.photo.url)
        # print(i.id)

        return JsonResponse({'id': i.id})

    return HttpResponse("")


# --- 資產維修詳細紀錄 ---

@login_required
@permission_required('asset.can_view_asset')
def asset_repair_detail(request, pk):
    if request.method == 'GET':
        print(pk)

        asset_repair_obj = models.AssetRepair.objects.get(id=pk)
        asset_repair_detail = models.AssetRepairDetail.objects.filter(repair=asset_repair_obj)

        # 過濾留言為技術部人員
        fix_users = list(
            set([i['user__code'] for i in asset_repair_detail.filter(user__dent__code='IT').values('user__code')]))
        print(fix_users)

        return render(request, 'asset_repair/detail.html', locals())

    if request.method == 'PUT':
        print("This is PUT")

        ret = {'status': '', 'code': '', 'msg': '', 'data': {}}

        put = QueryDict(request.body)
        print(put)

        # id = put.get('id')
        ststus = put.get('ststus')
        user = put.get('user')
        repair = put.get('repair')

        user = models.UserProfile.objects.get(id=user)
        print(user)

        if user.dent.code == 'IT':

            repair_obj = models.AssetRepair.objects.get(id=repair)

            print(ststus)

            if ststus == 'True':
                repair_obj.status = False
                repair_obj.repairer = None
                repair_obj.finish_date = None
                ret['data']['text'] = "跟進中"
                ret['data']['status'] = 'False'

            else:
                repair_obj.status = True
                repair_obj.repairer = request.user.userprofile
                repair_obj.finish_date = datetime.datetime.now()
                ret['data']['text'] = "已處理"
                ret['data']['status'] = 'True'

            repair_obj.save()

            ret['status'] = 'ok'
            ret['code'] = 200

        return JsonResponse(ret)


@login_required
@permission_required('asset.can_view_asset')
def asset_repair_detail_add(request):
    '''
    新增留言

    :param request:
    :return:
    '''
    if request.method == 'POST':
        print('Post')

        print(request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': ['asd'], 'content': ['adsasd'], 'user': ['314'], 'repair': ['19']}>

        froms_obj = forms.AssetRepairDetailForm(request=request, data=request.POST)
        # print(froms_obj.is_valid())
        # print(froms_obj.errors)

        if froms_obj.is_valid():
            ARD_obj = froms_obj.save()
            # print(froms_obj.cleaned_data)
            content = froms_obj.cleaned_data.get('content')
            user = froms_obj.cleaned_data.get('user')
            date = ARD_obj.create_date
            # print(date)
            # print(date.strftime("%Y/%m/%d %H:%M"))
            import pytz
            Shanghai = pytz.timezone(settings.TIME_ZONE)

            datetime.datetime.now()
            data = {
                'status': 'ok',
                'data':
                    {
                        'content': content,
                        'user': user.code,
                        'date': date.astimezone(Shanghai).strftime("%Y/%m/%d %H:%M")
                    },

            }

            return JsonResponse(data)

        # forms_obj = forms.AssetRepairDetailForm()
        # print(forms_obj)

        # froms_obj.save()


    elif request.method == 'PUT':
        print("this is put")


    else:
        print('else')
        return JsonResponse({})


@login_required
@permission_required('asset.can_view_asset')
def asset_repair_detail_edit(request):
    '''
    修改留言
    :param request:
    :return:
    '''

    if request.method == 'PUT':
        print("This is PUT")

        put = QueryDict(request.body)
        print(put)

        id = put.get('id')
        # content = put.get('content')
        # user = put.get('user')
        # repair = put.get('repair')

        repair_detail_obj = models.AssetRepairDetail.objects.get(id=id)

        froms_obj = forms.AssetRepairDetailForm(request=request, data=put, instance=repair_detail_obj)
        print(froms_obj.errors)
        if froms_obj.is_valid():

            if froms_obj.cleaned_data['user'] == repair_detail_obj.user:

                froms_obj.save()

                return JsonResponse({'status': 'ok', 'code': 200})

            else:

                return JsonResponse({'status': 'error', 'code': 201})

        return JsonResponse({})


@login_required
@permission_required('asset.can_view_asset')
def asset_repair_detail_del(request):
    '''
    刪除留言
    :param request:
    :return:
    '''

    print("This is Delete")
    put = QueryDict(request.body)
    id = put.get('id')
    dent_obj = models.AssetRepairDetail.objects.get(id=id)
    dent_obj.delete()

    return JsonResponse({'status': 'ok', 'code': 200})


# --- 部門 ---

@login_required
@permission_required('asset.can_view_department')
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


@login_required
@permission_required('asset.can_view_department')
def department_input(request):
    ret = {'status': '', "msg": '', 'errordict': {}}

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

        def foo(x):
            print('x', x)
            if not x:
                return x
            elif len(str(int(x))) < 3:
                return "%03d" % x
            else:
                return str(int(x))

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

        # 將user由int64轉成object
        df['user'] = df['user'].astype(object)
        # print(df.head())
        # print(df.info())

        # 將nan 轉為 '' 字符串
        df = df.astype(object).replace(np.nan, '')
        # 對user欄位 加工 帶入foo函數
        df['user'] = df['user'].map(foo)

        # print(df.head())
        rows = df.to_dict("record")

        for i, row in enumerate(rows):
            # print('row', row)

            forms_obj = forms.Dent_Input_Form(data=row)
            if forms_obj.is_valid():
                data_ret.append(forms_obj)
            else:
                print(forms_obj.errors)
                error = {i + 1: []}
                for k, v in forms_obj.errors.items():
                    # print(k, col_cn_name[k], row[k])
                    # print(v)
                    ret['status'] = 'error'
                    data = {'name': col_cn_name[k], 'message': v[0], 'content': row[k]}
                    error[i + 1].append(data)
                    # ret['msg'] += '%s "%s"錯誤' % (col_cn_name[e], row[e])
                    # data_ret = []
                ret['errordict'].update(error)

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


@login_required
@permission_required('asset.can_view_department')
def department_output(request):
    opts = models.Department.objects.all().model._meta

    file_name = r"demo_files/部門/DEMO_部門.xlsx"
    output_name = '%E9%83%A8%E9%96%80.xlsx'

    # ['ID', '部門名稱', '部門簡稱', '部門工/代號', '部門工/代號碼長度', '部門負責人']
    # row_names = [field.verbose_name for field in opts.fields]
    # print(row_names)

    # ['id', 'name', 'code', 'block_number', 'block_number_len', 'user']
    # field_names = [field.name for field in opts.fields]
    # print(field_names)

    data = [{field.verbose_name: getattr(obj, field.name) for field in opts.fields} for obj in
            models.Department.objects.all()]
    # print(data)
    df = pd.DataFrame(data)
    df.to_excel(file_name)

    file = open(file_name, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/vnd.ms-excel;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="%s"' % output_name

    return response


# --- 類型 ---

@login_required
@permission_required('asset.can_view_category')
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


@login_required
@permission_required('asset.can_view_category')
def category_input(request):
    ret = {'status': '', "msg": '', 'errordict': {}}

    if request.method == 'GET':
        return render(request, "category/input.html", locals())

    if request.method == 'POST':
        opts = models.Category.objects.all().model._meta

        # 存取檔案
        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        data_ret = []

        df = pd.read_excel(file.name)

        # ['ID','名稱', '代號']
        verbose_names = [field.verbose_name for field in opts.fields]
        verbose_names.remove('ID')

        # ['id','name', 'code']
        field_names = [field.name for field in opts.fields]
        field_names.remove('id')

        # 更改 column name
        col_name = {v: f for f, v in zip(field_names, verbose_names)}
        col_cn_name = {f: v for f, v in zip(field_names, verbose_names)}
        df = df.rename(columns=col_name)

        # 將nan 轉為 '' 字符串
        df = df.astype(object).replace(np.nan, '')
        print(df.head())

        rows = df.to_dict("record")
        # print(rows)

        for i, row in enumerate(rows):
            # print('row', row)

            forms_obj = forms.CaryForm(data=row)
            if forms_obj.is_valid():
                data_ret.append(forms_obj)
            else:
                print(forms_obj.errors)
                error = {i + 1: []}
                for k, v in forms_obj.errors.items():
                    # print(k, col_cn_name[k], row[k])
                    # print(v)
                    ret['status'] = 'error'
                    data = {'name': col_cn_name[k], 'message': v[0], 'content': row[k]}
                    error[i + 1].append(data)
                    # ret['msg'] += '%s "%s"錯誤' % (col_cn_name[e], row[e])
                    # data_ret = []
                ret['errordict'].update(error)

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            # print("data_ret", data_ret)
            for form in data_ret:
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


@login_required
@permission_required('asset.can_view_category')
def category_output(request):
    opts = models.Category.objects.all().model._meta
    # print(request)

    file_name = r'demo_files/類型/DEMO_類型.xlsx'
    output_name = "%E9%A1%9E%E5%9E%8B.xlsx"

    # ['ID', '名稱', '代號']
    # row_names = [field.verbose_name for field in opts.fields]

    # ['id', 'name', 'code']
    # field_names = [field.name for field in opts.fields]

    data = [{field.verbose_name: getattr(obj, field.name) for field in opts.fields} for obj in
            models.Category.objects.all()]

    print(data)
    df = pd.DataFrame(data)
    df.to_excel(file_name)

    file = open(file_name, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/vnd.ms-excel;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="%s"' % output_name

    return response


# --- 用戶 ---

@login_required
@permission_required('asset.can_view_userprofile')
def user(request):
    ret = {"status": "", "re_html": "", "msg": ""}
    search_field = {}

    user_obj = models.UserProfile.objects.all()
    sex_obj = models.UserProfile.sex_choice

    # print(sex_obj)

    dent_obj = models.Department.objects.all()

    # user forms表單
    form_obj = forms.User_Add_Form()

    if request.method == 'GET':
        # GET 字段

        print("GET")
        name = request.GET.get("name", '')
        sex = request.GET.get("sex", '')
        dent_id = request.GET.get("dent_id", '')
        contacts = request.GET.get('contacts', 10)

        search_field['name'] = name
        search_field['sex'] = sex
        search_field['dent_id'] = dent_id

        # GET 字段 篩選

        if sex and dent_id:
            user_obj = models.UserProfile.objects.filter(
                Q(name__contains=name) | Q(code__contains=name) | Q(user__username__contains=name),
                sex=sex,
                dent_id=dent_id
            )
        elif sex:
            user_obj = models.UserProfile.objects.filter(
                Q(name__contains=name) | Q(code__contains=name) | Q(user__username__contains=name),
                sex=sex
            )
        elif dent_id:
            user_obj = models.UserProfile.objects.filter(
                Q(name__contains=name) | Q(code__contains=name) | Q(user__username__contains=name),
                dent_id=dent_id
            )
        else:
            user_obj = models.UserProfile.objects.filter(
                Q(name__contains=name) | Q(code__contains=name) | Q(user__username__contains=name)
            )

        # 分頁功能

        search_field['contacts'] = contacts
        paginator = Paginator(user_obj, contacts)  # Show 10 contacts per page

        page = request.GET.get('page', 1)
        try:
            user_obj = paginator.page(page)
        except PageNotAnInteger:
            user_obj = paginator.page(1)
        except EmptyPage:
            user_obj = paginator.page(paginator.num_pages)

        return render(request, 'user/index.html', locals())

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


@login_required
@permission_required('asset.can_view_userprofile')
def user_info(request):
    pass


@login_required
@permission_required('asset.can_view_userprofile')
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

            # print(user)

            dent = user_obj.userprofile.dent.code

            perms_list = [i.split('.') for i in roles.perms.get(dent) or roles.perms.get('other')]

            print('perms_list', perms_list)
            # print(perms_list)

            perms_obj = [Permission.objects.get(content_type__model=model, codename=codename) for model, codename in
                         perms_list]
            print(perms_obj)

            user_obj.user_permissions = perms_obj

            # print("ok")
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


@login_required
@permission_required('asset.can_view_userprofile')
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


@login_required
@permission_required('asset.can_view_userprofile')
def user_input(request):
    ret = {'status': '', "msg": '', 'errordict': {}}

    if request.method == 'GET':
        return render(request, "user/input.html", locals())

    if request.method == 'POST':
        opts = models.UserProfile.objects.all().model._meta

        # 存取檔案
        print(request)
        file = request.FILES['file']
        with open(file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 分析
        data_ret = []

        # 讀取excel
        df = pd.read_excel(file.name)

        # <class 'list'>:['ID', '用户名', '姓名', '員工編號', '員工號碼', '性別', '部門', '在職狀態', '生日日期']
        verbose_names = [field.verbose_name for field in opts.fields]
        print(verbose_names)
        verbose_names.remove('ID')

        # <class 'list'>: ['id', 'user', 'name', 'code', 'number', 'sex', 'dent', 'in_service', 'birthday']
        field_names = [field.name for field in opts.fields]
        print(field_names)
        field_names.remove('id')

        # 更改 column name
        col_name = {v: f for f, v in zip(field_names, verbose_names)}
        col_cn_name = {f: v for f, v in zip(field_names, verbose_names)}
        df = df.rename(columns=col_name)

        # 將user由int64轉成object
        df['code'] = df['code'].astype(object)
        # 將nan 轉為 '' 字符串
        df = df.astype(object).replace(np.nan, '')
        rows = df.to_dict("record")

        for i, row in enumerate(rows):
            # print('row', row)

            forms_obj = forms.UserProfile_Input_Form(data=row)
            if forms_obj.is_valid():
                data_ret.append(forms_obj)
            else:
                print(forms_obj.errors)
                error = {i + 1: []}
                for k, v in forms_obj.errors.items():
                    # print(k, col_cn_name[k], row[k])
                    # print(v)
                    ret['status'] = 'error'
                    data = {'name': col_cn_name[k], 'message': v[0], 'content': row[k]}
                    error[i + 1].append(data)
                    # ret['msg'] += '%s "%s"錯誤' % (col_cn_name[e], row[e])
                    # data_ret = []
                ret['errordict'].update(error)

        # 匯入
        if ret['status'] == 'error':
            pass
        else:
            # print("data_ret", data_ret)
            for form in data_ret:
                form.save()
            ret['status'] = 'ok'
            ret['msg'] = '匯入成功'

        # 必須傳回JSON
        return JsonResponse(ret)


@login_required
@permission_required('asset.can_view_userprofile')
def user_output(request):
    opts = models.UserProfile.objects.all().model._meta

    file_name = r'demo_files/用戶/DEMO_用戶.xlsx'
    output_name = "%E7%94%A8%E6%88%B6.xlsx"

    # ['ID', '用户名', '姓名', '員工編號', '員工號碼', '性別', '部門', '在職狀態', '生日日期']
    # row_names = [field.verbose_name for field in opts.fields]

    # ['id', 'user', 'name', 'code', 'number', 'sex', 'dent', 'in_service', 'birthday']
    # fields = [field.name for field in opts.fields]

    data = [{field.verbose_name: getattr(obj, field.name) for field in opts.fields} for obj in
            models.UserProfile.objects.all()]

    df = pd.DataFrame(data)

    # 刪除欄位
    df = df.drop('ID', axis=1)
    df = df.drop('員工號碼', axis=1)

    df.to_excel(file_name)

    file = open(file_name, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/vnd.ms-excel;charset=utf-8'
    response['Content-Disposition'] = 'attachment;filename="%s"' % output_name

    return response


# --- 新聞---

def news(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == "GET":

        ret = {"status": "", "re_html": "", "msg": ""}

        search_field = {}

        name = request.GET.get('name', "")
        dent_id = request.GET.get('dent_id')
        status = request.GET.get('status')

        dent_obj = models.Department.objects.all()

        # 驗證用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        if request.user.userprofile.dent in admindent:
            print('管理用戶')
            # category_obj = models.Category.objects.all()
            news_obj = models.News.objects.all()
            # user_obj = models.UserProfile.objects.all()
        else:
            news_obj = models.News.objects.filter(dent=request.user.userprofile.dent).all()

        if dent_id and status:
            # news_obj = news_obj.filter(dent_id=dent_id).all()
            get_dent_obj = models.Department.objects.get(id=dent_id)
            news_obj = news_obj.filter(title__contains=name, creator__dent=get_dent_obj)
            if status == 'y':
                news_obj = news_obj.filter(userprofile__user_id=request.user.id)
            elif status == 'n':
                news_obj = news_obj.exclude(userprofile__user_id=request.user.id)
        elif dent_id:
            get_dent_obj = models.Department.objects.get(id=dent_id)
            news_obj = news_obj.filter(title__contains=name, creator__dent=get_dent_obj)
        elif status:
            if status == 'y':
                news_obj = news_obj.filter(userprofile__user_id=request.user.id)
            elif status == 'n':
                news_obj = news_obj.exclude(userprofile__user_id=request.user.id)
        else:
            pass

        # 分頁功能
        paginator = Paginator(news_obj, 10)  # Show 10 contacts per page

        page = request.GET.get('page')
        try:
            news_obj = paginator.page(page)
        except PageNotAnInteger:
            news_obj = paginator.page(1)
        except EmptyPage:
            news_obj = paginator.page(paginator.num_pages)

        return render(request, 'news/index.html', locals())

    if request.method == 'DELETE':
        print("THIS IS DELETE")
        put = QueryDict(request.body)
        print(put)
        id = put.get('id')
        news_obj = models.News.objects.get(id=id)
        news_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)


def news_add(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':
        forms_obj = forms.NewsForm(request=request)
        return render(request, 'news/add.html', locals())

    if request.method == 'POST':
        forms_obj = forms.NewsForm(request=request, data=request.POST)
        print(request.POST)
        if forms_obj.is_valid():
            news_obj = forms_obj.save()
            dents = forms_obj.cleaned_data.get('dent')
            for dent_obj in dents:
                news_obj.dent.add(dent_obj)
            news_obj.userprofile.add(request.user.userprofile)
            return redirect("news")


def news_edit(request, pk):
    if request.method == 'GET':
        news_obj = models.News.objects.get(id=pk)

        # 驗證用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        if request.user.userprofile.dent in news_obj.dent.all() or request.user.userprofile.dent in admindent:
            forms_obj = forms.NewsForm(request=request, instance=news_obj)
            return render(request, 'news/add.html', locals())
        else:
            return redirect("news")

    if request.method == 'POST':
        news_obj = models.News.objects.get(id=pk)

        forms_obj = forms.NewsForm(request=request, data=request.POST, instance=news_obj)
        if forms_obj.is_valid():
            dents = forms_obj.cleaned_data.get('dent')
            news_obj = forms_obj.save()
            news_obj.dent.clear()
            for dent_obj in dents:
                news_obj.dent.add(dent_obj)
            return redirect("news")


def news_info(request, pk):
    if request.method == 'GET':

        news_obj = models.News.objects.get(id=pk)
        # 驗證用戶
        admindent = models.Department.objects.filter(code__in=['OM', 'HR'])
        if request.user.userprofile.dent in news_obj.dent.all() or request.user.userprofile.dent in admindent:
            news_obj.userprofile.add(request.user.userprofile)
            news_obj.save()
            return render(request, 'news/info.html', locals())
        else:
            return redirect("news")


# --- 登入/登出 ---

def acc_login(request):
    error_msg = ""

    if request.method == 'GET':

        # 判斷是否已登入
        if request.user.is_authenticated():
            return redirect(request.GET.get('next', '/asset'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            return redirect(request.GET.get('next', '/asset'))

        else:
            error_msg = "使用者或密碼有誤!!"

        print(user, username, password)

    return render(request, 'login.html', {'error_msg': error_msg})


def acc_logout(request):
    logout(request)
    print("logout")
    return redirect('/login')


# --- ---


# redirect
def home_redirect(request):
    return HttpResponseRedirect(
        reverse('asset')
    )


# --- 個人首頁 ---

@login_required
def userprofile(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    userinfo_obj = request.user.userprofile

    print("request.method", request.method)

    if request.method == 'GET':
        # forms_user_obj = forms.User_Edit_Form(instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfile_Edit_Form(instance=userinfo_obj, request=request)

    elif request.method == 'POST':

        print("request.POST", request.POST)

        # forms_user_obj = forms.User_Edit_Form(request.POST, instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfile_Edit_Form(request.POST, instance=userinfo_obj, request=request)

        fields = set(list(dict(forms_userproinfo_obj.fields).keys()))
        errors = set(dict(forms_userproinfo_obj.errors.keys()))
        print(fields)
        print(errors)

        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)

        # 確認表單提交無誤
        if forms_userproinfo_obj.is_valid():
            # 把判斷都交給Form表單並儲存
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

    return render(request, 'userprofile.html', locals())


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
    remote_ip = request.META['REMOTE_ADDR']
    print(remote_ip)

    return HttpResponse("")


def formatdata(request):
    from test_script import create01_dent_data, create02_admin, create03_user_data, create04_data, create05_asset_data
    create01_dent_data.main()
    create02_admin.main()
    create03_user_data.main()
    create04_data.main()
    create05_asset_data.main()

    return HttpResponse("OK")


@login_required
def user_permission(request):
    # user = request.user
    # print(user)

    # p = Permission.objects.all()
    #
    # print(p)

    '''
    p = Permission.objects.all()
    for i in p:
        # print(i)
        # print()
        print("%s.%s" % (i.content_type.model,i.codename))

    '''

    # request.user.user_permissions.clear()
    # print(request.user.get_all_permissions())

    dent = request.user.userprofile.dent.code

    perms_list = [i.split('.') for i in roles.perms.get(dent) or roles.perms.get('other')]

    print('perms_list', perms_list)
    # p = Permission.objects.get(content_type__model='asset',codename='can_view_asset')
    # print(p)
    # p = Permission.objects.get(content_type__model='host',codename='can_view_host')
    # print(p)
    # p = Permission.objects.get(content_type__model='location',codename='can_view_location')
    # print(p)
    # # p = Permission.objects.get(content_type__model='host',codename='can_view_host')
    # # print(p)
    #
    # # perm_list =
    #
    # # request.user.get_all_permissions()
    # #
    # # for i in Permission.objects.all():
    # #     print(i.content_type.model,i.codename)
    #
    # # acan = Permission.objects.filter(content_type__model='asset',codename='can_view_asset')
    # # print(acan)
    #
    # # p = Permission.objects.get(content_type__model='asset', codename='can_view_asset')
    # # print(p)
    #
    #
    # #
    # #
    # #
    perms_obj = [Permission.objects.get(content_type__model=model, codename=codename) for model, codename in perms_list]
    print('perms_obj', perms_obj)
    # #
    request.user.user_permissions = perms_obj

    return HttpResponse(request.user.username)
