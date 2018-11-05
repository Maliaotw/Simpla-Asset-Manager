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
from django.conf.urls import url, include
from django.contrib import admin

from asset import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # --- asset ---
    url(r'^asset/$', views.asset, name="asset"),

    url(r'^asset/add', views.asset_add, name="asset_add"),
    url(r'^asset/edit/(?P<pk>\d+)', views.asset_edit, name="asset_edit"),
    url(r'^asset/asset_input', views.asset_input, name="asset_input"),
    url(r'^asset/asset_output', views.asset_output, name="asset_output"),




    url(r'^department/$', views.department, name="department"),
    url(r'^category/$', views.category, name="category"),


    # --- user ---
    url(r'^user/$', views.user, name="user"),
    url(r'^user/(\d+)', views.user_info, name="user_info"),
    url(r'^user/add', views.user_add, name="user_add"),
    url(r'^user/edit/(?P<pk>\d+)', views.user_edit, name="user_edit"),
    url(r'^user/user_input', views.user_input, name="user_input"),
    url(r'^user/user_output', views.user_output, name="user_output"),


    # delete

    url(r'^test1/', views.test1, name="test1"),
    url(r'^test2/', views.test2, name="test2"),

]
