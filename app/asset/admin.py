from django.contrib import admin

from asset import models


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'code','dent']
    list_filter = ['dent']

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Category)
admin.site.register(models.Location)
admin.site.register(models.Department)
admin.site.register(models.Asset)
admin.site.register(models.AssetRecord)
admin.site.register(models.AssetRepair)
# admin.site.register(models.AssetRepairDetail)
admin.site.register(models.AssetRepairDetail)
admin.site.register(models.AssetRepairImage)
admin.site.register(models.BusinessUnit)
admin.site.register(models.AssetBusiness)
admin.site.register(models.News)
admin.site.register(models.AssetToAssets)
