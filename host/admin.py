from django.contrib import admin
from host import models
# Register your models here.

admin.site.register(models.Host)
admin.site.register(models.NIC)
admin.site.register(models.Disk)
admin.site.register(models.Memory)
admin.site.register(models.HostRecord)