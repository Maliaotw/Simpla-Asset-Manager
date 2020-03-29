"""AutoCmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import include, path

from asset import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # --- homepage ---


    # --- asset ---
    path('asset/', views.asset, name="asset"),
    # url(r'^asset/index$', views.asset_index, name="asset_index"),
    path('asset/index/', views.AssetListView.as_view(), name="asset_list"),

    # url(r'^asset/add', views.asset_add, name="asset_add"),
    path('asset/create', views.AssetCreateView.as_view(), name="asset_create"),
    path('asset/<int:pk>/update/', views.AssetUpdateView.as_view(), name="asset_update"),
    # url(r'^asset/input', views.asset_input, name="asset_input"),
    # url(r'^asset/output', views.asset_output, name="asset_output"),
    path('asset/busunit', views.asset_busunit, name="asset_busunit"),

    # --- asset_repair ---
    path('asset/repair', views.asset_repair, name='asset_repair'),
    path('asset/repair/add', views.asset_repair_add, name='asset_repair_add'),
    path('asset/repair/detail/<int:pk>', views.asset_repair_detail, name="asset_repair_detail"),

    path('asset_file', views.asset_file, name='asset_file'),

    # --- asset_repair_detail ---
    path('asset_repair_detail/add', views.asset_repair_detail_add, name="asset_repair_detail_add"),
    path('asset_repair_detail/edit', views.asset_repair_detail_edit, name="asset_repair_detail_edit"),
    path('asset_repair_detail/del', views.asset_repair_detail_del, name="asset_repair_detail_del"),

    # --- Asset_relation_Assets

    path('asset/ara', views.ara, name="ara_index"),

    # --- department ---
    path('department', views.department, name="department"),
    path('department/input', views.department_input, name="department_input"),
    path('department/output', views.department_output, name="department_output"),

    # --- category ---
    path('category', views.category, name="category"),
    path('category/input', views.category_input, name="category_input"),
    path('category/output', views.category_output, name="category_output"),

    # --- user ---
    path('user', views.user, name="user"),
    path('user/(\d+)', views.user_info, name="user_info"),
    path('user/add', views.user_add, name="user_add"),
    path('user/edit/(?P<pk>\d+)/$', views.user_edit, name="user_edit"),
    path('user/input', views.user_input, name="user_input"),
    path('user/output', views.user_output, name="user_output"),

    # --- userprofile ---
    path('userprofile/$', views.userprofile, name="userprofile"),

    # --- bus ---
    path('busunit', views.busunit, name="busunit"),

    # --- news ---
    path('news/index', views.news, name="news"),
    path('news/add', views.news_add, name="news_add"),
    path('news/edit/(?P<pk>\d+)/$', views.news_edit, name="news_edit"),
    path('news/(?P<pk>\d+)/$', views.news_info, name="news_info"),

    # test

    # url(r'^test1/', views.test1, name="test1"),
    # url(r'^test2/', views.test2, name="test2"),
    # url(r'^user_permissions/', views.user_permission, name="user_permissions"),
    # url(r'^formatdata/', views.formatdata, name="formatdata"),

]
