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
# from django.conf.urls import url, include
from django.contrib import admin
from django.urls import include, path
from host import views
from asset.views import asset_repair_detail

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # --- host ---
    path('host', views.host, name="host"),
    path('host/index', views.host_index, name="host_index"),
    path('host/repair', views.host_repair, name="host_repair"),


    path('host/repair/detail/<int:pk>', views.host_repair_detail, name="host_repair_detail"),



    path('host/<int:pk>', views.host_info, name="host_info"),
    path('host/input', views.host_input, name="host_input"),
    path('host/output', views.host_output, name="host_output"),

    # --- network ---

    # --- location ---
    path('location/', views.location, name="location"),

    path('demo1/', views.demo1),

]
