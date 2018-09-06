from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    '''用戶'''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64, verbose_name="暱稱")

    def __str__(self):
        return self.name

class Position(models.Model):
    '''
    主機位置表
    '''
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "主機位置表"

    def __str__(self):
        return self.name


class Department(models.Model):
    '''
    部門資產表
    '''
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "部門資產表"

    def __str__(self):
        return self.name


class Asset(models.Model):
    '''
    資產信息表
    '''

    davice_type_choice = (
        (1, '工作站'),
        (2, '值班電腦'),
        (3, '培訓電腦'),
        (4, '備用電腦'),
        (5, '汰換機'),
        (6, '測試機'),

    )

    device_type_id = models.IntegerField(choices=davice_type_choice, default=2)

    position = models.ForeignKey('Position', verbose_name='主機位置', null=True, blank=True)
    department = models.ForeignKey('Department', verbose_name='部門', null=True, blank=True)

    latest_data = models.DateField(null=True)
    creare_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "資產表"

    def __str__(self):
        return "%s %s" % (self.department, self.host)


class Host(models.Model):
    """
    主機信息
    """
    asset = models.OneToOneField('Asset')

    name = models.CharField(max_length=128, unique=True)
    sn = models.CharField('SN', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='製造商', max_length=64, null=True, blank=True)
    model = models.CharField('型號', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('IP', null=True, blank=True)

    os_platform = models.CharField('系統', max_length=16, null=True, blank=True)
    os_version = models.CharField('系統版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('邏輯處理器', null=True, blank=True)
    cpu_physical_count = models.IntegerField('處理器內核', null=True, blank=True)
    cpu_model = models.CharField('處理器型號', max_length=128, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "主機表"

    def __str__(self):
        return self.name


class NIC(models.Model):
    '''
    網卡表
    '''
    name = models.CharField('網卡名稱', max_length=255, null=True, blank=True)
    ipaddress = models.GenericIPAddressField('IP', blank=True, null=True)
    model = models.CharField('型號', max_length=255, null=True, blank=True)
    macaddress = models.CharField('MAC', max_length=255, null=True, blank=True)
    netmask = models.CharField('Netmask', max_length=255, null=True, blank=True)
    host_obj = models.ForeignKey("Host", related_name='nic')

    class Meta:
        verbose_name_plural = "網卡表"


    def __str__(self):
        return self.ipaddress


class Disk(models.Model):
    """
    硬盤信息表
    """
    slot = models.CharField('插槽位置', max_length=8)
    model = models.CharField('硬盤型號', max_length=64)
    capacity = models.FloatField('硬盤容量')
    host_obj = models.ForeignKey("Host", related_name='disk')

    class Meta:
        verbose_name_plural = "硬盤表"

    def __str__(self):
        return "%s %s" % (self.model,self.capacity)


class Memory(models.Model):
    """
    内存信息表
    """
    slot = models.CharField('插槽位置', max_length=32)
    manufacturer = models.CharField('製造商', max_length=32, null=True, blank=True)
    model = models.CharField('型號', max_length=64)
    capacity = models.FloatField('內存容量', null=True, blank=True)
    sn = models.CharField('內存SN號', max_length=64, null=True, blank=True)

    host_obj = models.ForeignKey("Host", related_name='memory')

    class Meta:
        verbose_name_plural = "内存表"

    def __str__(self):
        return "%s %s" % (self.model,self.capacity)


class AssetRecord(models.Model):
    """
    資產變更紀錄表
    """
    asset_obj = models.ForeignKey('Asset', related_name='asset')
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True)
    creator = models.ForeignKey('UserProfile', null=True, blank=True)

    # 狀態: 處理完成 或 需跟進
    status = models.BooleanField(default=True)

    # 類型: 自動上傳，IT維護，故障報修
    assetrecord_type_choice = (
        (1, '自動上傳'),
        (2, 'IT維護'),
        (3, '故障報修'),
    )

    assetrecord_type_id = models.IntegerField(choices=assetrecord_type_choice, default=2)

    # 檔案: 圖片 多對多
    photo = models.ManyToManyField('AssetRecordImage', null=True, blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    finish_data = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "資產紀錄表"

    def __str__(self):
        return "%s" % (self.asset_obj.host.name)

class AssetRecordDetail(models.Model):
    '''
    資產變更詳細紀錄表
    '''
    content = models.TextField()
    user = models.ForeignKey('UserProfile')
    record = models.ForeignKey('AssetRecord')
    create_date = models.DateTimeField(auto_now_add=True)
    photo = models.ManyToManyField('AssetRecordImage', null=True, blank=True)

    class Meta:
        verbose_name_plural = "資產變更詳細紀錄表"

    def __str__(self):
        return "%s %s" % (self.record,self.user)

class AssetRecordImage(models.Model):
    '''
    資產變更關聯圖片表
    '''

    name = models.CharField(max_length=255)
    photo = models.ImageField()

    class Meta:
        verbose_name_plural = "資產變更詳細紀錄表"

    def __str__(self):
        return "%s" % (self.name)






