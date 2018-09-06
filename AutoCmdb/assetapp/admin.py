from django.contrib import admin

from assetapp import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Position)
admin.site.register(models.Department)
admin.site.register(models.Asset)
admin.site.register(models.Host)
admin.site.register(models.NIC)
admin.site.register(models.Disk)
admin.site.register(models.Memory)
admin.site.register(models.AssetRecord)
admin.site.register(models.AssetRecordDetail)