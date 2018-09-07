from django.contrib import admin

from asset import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Location)
admin.site.register(models.Department)
admin.site.register(models.Asset)
admin.site.register(models.AssetHost)
admin.site.register(models.AssetRecord)
admin.site.register(models.AssetRecordDetail)
admin.site.register(models.AssetRecordImage)