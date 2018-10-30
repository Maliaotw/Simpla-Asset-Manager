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
    url(r'^asset/(\d+)$', views.asset_info, name="asset_info"),
    url(r'^asset/add', views.asset_add, name="asset_add"),
    url(r'^asset/edit/(?P<pk>\d+)', views.asset_edit, name="asset_edit"),

    url(r'^department/$', views.department, name="department"),
    url(r'^category/$', views.category, name="category"),


    # --- user ---
    url(r'^user/$', views.user, name="user"),
    url(r'^user/(\d+)', views.user_info, name="user_info"),
    url(r'^user/add', views.user_add, name="user_add"),
    url(r'^user/edit/(?P<pk>\d+)', views.user_edit, name="user_edit"),
    # delete

    url(r'^test1/', views.test1, name="test1"),
    url(r'^test2/', views.test2, name="test2"),

]
