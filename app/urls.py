"""AutoCmdb path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path(r'^$', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.conf.paths import path, include
    2. Add a path to pathpatterns:  path(r'^blog/', include('blog.paths'))
"""
# from django.conf.paths import path, include # 1.0
from django.contrib import admin
# from django.conf.urls.static import static
# from django.conf import settings
# from django.views.static import serve
from django.urls import include, path

from asset.views import acc_login, acc_logout
# from api import views

urlpatterns = [
    path('login/', acc_login, name="login"),
    path('logout/', acc_logout, name="logout"),
    # path('admin/', admin.site.paths),
    path('', include('host.urls')),
    path('api/', include('api.urls')),
    path('', include('asset.urls')),
    # path('media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # static(settings.DEMO_path, document_root=settings.DEMO_ROOT)[0],
    # static(settings.STATIC_path, document_root=settings.STATIC_ROOT)[0]
]
