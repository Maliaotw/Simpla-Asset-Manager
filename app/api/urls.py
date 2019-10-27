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

from api import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^category/', views.category),
    url(r'^dent_user/', views.dent_user),
    url(r'^add_user_number/', views.add_user_number),
    url(r'^asset_no_hostname/', views.asset_no_hostname),
    url(r'^asset_by_hostname/', views.asset_by_hostname),

    url(r'^host/', views.host),

    url(r'^ardtohtml/', views.ardtohtml, name='ardtohtml'),

]
