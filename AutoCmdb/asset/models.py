from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    '''
    用戶
    '''

    user = models.OneToOneField(User, verbose_name="用户名")
    name = models.CharField(max_length=64, verbose_name="姓名")
    code = models.CharField(max_length=64, verbose_name='員工編號', blank=True, null=True)
    number = models.CharField(max_length=64, verbose_name='員工號碼', blank=True, null=True)

    sex_choice = (
        ('男', '男'),
        ('女', '女'),
    )

    sex = models.CharField(verbose_name='性別', choices=sex_choice, max_length=16)
    dent = models.ForeignKey('Department', verbose_name='部門', blank=True, null=True)

    in_service_choice = (
        ('在職', '在職'),
        ('離職', '離職'),
        ('停職', '停職'),
        ('退休', '退休'),
    )

    in_service = models.CharField(verbose_name='在職狀態', choices=in_service_choice, max_length=64)
    birthday = models.DateField(null=True, blank=True, verbose_name='生日日期')

    class Meta:
        verbose_name_plural = "用戶"

        permissions = (
            ("can_view_userprofile", "Can view UserProfile"),
            ("can_change_userprofile", "Can change UserProfile"),
        )

    def __str__(self):
        return "%s(%s)" % (self.code, self.user.username,)


class Location(models.Model):
    '''
    位置
    '''
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "位置"

        permissions = (
            ("can_view_location", "Can view location"),
        )

    def __str__(self):
        return self.name


class Department(models.Model):
    '''
    部門
    '''

    name = models.CharField(max_length=255, verbose_name="部門名稱")
    code = models.CharField(max_length=128, verbose_name='部門簡稱')
    block_number = models.CharField(max_length=128, verbose_name='部門工/代號')
    block_number_len = models.PositiveIntegerField(verbose_name='部門工/代號碼長度')
    user = models.ForeignKey('UserProfile', verbose_name='部門負責人', blank=True, null=True)

    class Meta:
        verbose_name_plural = "部門"

        permissions = (
            ("can_view_department", "Can view department"),
        )

    def __str__(self):
        return "%s部(%s)" % (self.name, self.code)


class Category(models.Model):
    '''
    分類
    '''
    name = models.CharField(max_length=255, verbose_name='名稱')
    code = models.CharField(max_length=255, verbose_name='代號')

    class Meta:
        verbose_name_plural = "類型"

        permissions = (
            ("can_view_category", "Can view category"),
        )

    def __str__(self):
        return "%s(%s)" % (self.code, self.name)


class Asset(models.Model):
    '''
    資產信息表
    '''

    name = models.CharField(verbose_name='資產編號', max_length=255)
    number = models.IntegerField(verbose_name='資產號碼', max_length=255)
    price = models.IntegerField(verbose_name='價格', null=True, blank=True)
    category = models.ForeignKey("category", verbose_name='類型')
    department = models.ForeignKey('Department', verbose_name='部門', null=True, blank=True)
    manager = models.ForeignKey("UserProfile", verbose_name='負責人', null=True, blank=True)
    purchase_date = models.DateField(verbose_name='購買日期', null=True, blank=True)

    status_choice = (
        ('未使用', '未使用'),
        ('使用中', '使用中'),
        ('遺失', '遺失'),
        ('報廢', '報廢'),
    )

    status = models.CharField(verbose_name='狀態', max_length=16, choices=status_choice, default='未使用')

    latest_date = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    create_date = models.DateTimeField(verbose_name='創建日期', auto_now_add=True)

    class Meta:
        verbose_name_plural = "資產信息表"

        permissions = (
            ("can_view_asset", "Can view asset"),
        )

    def __str__(self):
        return "%s" % (self.name)


class AssetRecord(models.Model):
    """
    TODO 待刪除
    資產變更紀錄表
    """
    asset_obj = models.ForeignKey('Asset')
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
    creator = models.ForeignKey('UserProfile', verbose_name='創建者', null=True, blank=True, related_name='creator')

    # 類型: 自動上傳，IT維護
    type_choice = (
        (1, '自動上傳'),
        (2, 'IT維護'),
    )

    type = models.IntegerField(choices=type_choice, default=0)

    create_date = models.DateTimeField(auto_now_add=True, verbose_name='創建日期')

    class Meta:
        verbose_name_plural = "資產紀錄表"

    def __str__(self):
        return "%s" % (self.asset_obj)


class AssetRepair(models.Model):
    '''
    資產維修紀錄表
    '''

    asset_obj = models.ForeignKey('Asset', verbose_name='資產編號')
    title = models.CharField(max_length=255, verbose_name='標題')
    summary = models.TextField(verbose_name='內文', null=True, blank=True)

    creator = models.ForeignKey('UserProfile', verbose_name='創建者', null=True, blank=True, related_name='+')

    # 狀態: 處理完成 或 需跟進
    status = models.BooleanField(default=False)

    # 維修者：最後是誰修理完成的
    repairer = models.ForeignKey('UserProfile', verbose_name='維修者', null=True, blank=True, related_name='+')

    # 檔案: 圖片 多對多
    photo = models.ManyToManyField('AssetRepairImage', null=True, blank=True)

    create_date = models.DateTimeField(auto_now_add=True, verbose_name='創建日期')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='完成日期')

    class Meta:
        verbose_name_plural = "資產維修表"

    def __str__(self):
        return "%s" % (self.asset_obj)


class AssetRepairDetail(models.Model):
    '''
    資產變更詳細紀錄表
    '''

    content = models.TextField()
    user = models.ForeignKey('UserProfile')
    repair = models.ForeignKey('AssetRepair')
    create_date = models.DateTimeField(auto_now_add=True)
    photo = models.ManyToManyField('AssetRepairImage', null=True, blank=True)

    class Meta:
        verbose_name_plural = "資產維修詳細紀錄表"

    def __str__(self):
        return "%s %s %s" % (self.repair, self.user.code, self.content)


class AssetRepairImage(models.Model):
    '''
    資產變更關聯圖片表
    '''

    name = models.CharField(max_length=255)
    photo = models.ImageField()

    class Meta:
        verbose_name_plural = "資產紀錄圖片表"

    def __str__(self):
        return "%s" % (self.name)
