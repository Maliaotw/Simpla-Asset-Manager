from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    '''
    用戶
    '''

    user = models.OneToOneField(User)
    name = models.CharField(max_length=64, verbose_name="暱稱")
    code = models.IntegerField(verbose_name='員工編號',blank=True,null=True)

    sex_choice = (
        (1, '男'),
        (2, '女'),
    )

    sex = models.IntegerField(choices=sex_choice)
    dent = models.ForeignKey('Department',verbose_name='部門',blank=True,null=True)

    class Meta:
        verbose_name_plural = "用戶"

    def __str__(self):
        return self.name


class Location(models.Model):
    '''
    位置
    '''
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "位置"

    def __str__(self):
        return self.name


class Department(models.Model):
    '''
    部門
    '''
    name = models.CharField(max_length=255,verbose_name="部門名稱")
    code = models.CharField(max_length=128,verbose_name='部門簡稱')
    block_number = models.CharField(max_length=128,verbose_name='部門工/代號')
    block_number_len = models.PositiveIntegerField(verbose_name='部門工/代號碼長度')
    user = models.ForeignKey('UserProfile',verbose_name='部門負責人',blank=True,null=True)


    class Meta:
        verbose_name_plural = "部門"

    def __str__(self):
        return "%s部(%s)" % (self.name,self.code)


class Catagory(models.Model):
    '''
    分類
    '''
    name = models.CharField(max_length=255,verbose_name='名稱')
    code = models.CharField(max_length=255,verbose_name='代號')

    class Meta:
        verbose_name_plural = "類型"

    def __str__(self):
        return "%s(%s)" % (self.name,self.code)


class Asset(models.Model):
    '''
    資產信息表
    '''

    sn = models.CharField(max_length=255)
    price = models.IntegerField(verbose_name='價格', null=True, blank=True)
    category = models.ForeignKey("Catagory",verbose_name='類型')
    department = models.ForeignKey('Department', verbose_name='部門', null=True, blank=True)
    manager = models.ForeignKey("UserProfile", verbose_name='負責人', null=True, blank=True)
    latest_date = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    create_date = models.DateTimeField(verbose_name='創建日期',auto_now_add=True)

    class Meta:
        verbose_name_plural = "資產信息表"

    def __str__(self):
        return "%s %s-%s" % (self.department, self.category.code,self.sn)


class AssetRecord(models.Model):
    """
    資產變更紀錄表
    """
    asset_obj = models.ForeignKey('Asset', related_name='asset')
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
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

    create_date = models.DateTimeField(auto_now_add=True,verbose_name='創建日期')
    finish_date = models.DateTimeField(null=True, blank=True,verbose_name='完成日期')

    class Meta:
        verbose_name_plural = "資產紀錄表"

    def __str__(self):
        return "%s" % (self.asset_obj)


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
        return "%s %s" % (self.record, self.user)


class AssetRecordImage(models.Model):
    '''
    資產變更關聯圖片表
    '''

    name = models.CharField(max_length=255)
    photo = models.ImageField()

    class Meta:
        verbose_name_plural = "資產紀錄圖片表"

    def __str__(self):
        return "%s" % (self.name)
