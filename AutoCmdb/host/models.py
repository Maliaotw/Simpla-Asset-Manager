from django.db import models

# Create your models here.


class Host(models.Model):
    '''
    主機資產表
    '''

    status_choice = (
        ('工作站', '工作站'),
        ('值班電腦', '值班電腦'),
        ('培訓電腦', '培訓電腦'),
        ('備用電腦', '備用電腦'),
        ('汰換機', '汰換機'),
        ('測試機', '測試機'),
    )

    asset = models.OneToOneField('asset.Asset',verbose_name="資產編號",null=True,blank=True ,related_name='Host')
    ops_owner = models.ForeignKey('asset.UserProfile',verbose_name="運維負責人",null=True, blank=True)
    location = models.ForeignKey('asset.Location', verbose_name='位置', null=True, blank=True)

    status = models.CharField(choices=status_choice, default='值班電腦',max_length=64)

    name = models.CharField(verbose_name="主機名稱",max_length=64)
    number = models.IntegerField(verbose_name="主機號碼")

    sn = models.CharField('SN序號', max_length=64, null=True, blank=True)
    pn = models.CharField('產品序號', max_length=64, null=True, blank=True) # 保固用

    manufacturer = models.CharField(verbose_name='製造商', max_length=64, null=True, blank=True)
    model = models.CharField('型號', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('IP', null=True, blank=True)

    os_distribution = models.CharField('發行版本', max_length=64, blank=True, null=True)
    os_platform = models.CharField('系統', max_length=16, null=True, blank=True)
    os_version = models.CharField('系統版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('邏輯處理器', null=True, blank=True)
    cpu_physical_count = models.IntegerField('處理器內核', null=True, blank=True)
    cpu_model = models.CharField('處理器型號', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "主機資產表"

    def __str__(self):
        return "%s %s" % (self.number,self.manage_ip)


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
        return "%s %s" % (self.host_obj, self.ipaddress)


class Disk(models.Model):
    """
    硬盤信息表
    """
    slot = models.CharField('插槽位置', max_length=8)
    model = models.CharField('硬盤型號', max_length=64,null=True, blank=True)
    capacity = models.FloatField('硬盤容量')
    host_obj = models.ForeignKey("Host", related_name='disk')
    sn = models.CharField("硬碟序號",max_length=128,null=True, blank=True)
    manufacturer = models.CharField('製造商', max_length=32, null=True, blank=True)
    iface_type = models.CharField('接口類型', max_length=64)

    class Meta:
        verbose_name_plural = "硬盤表"

    def __str__(self):
        return "%s %s" % (self.host_obj, self.capacity)


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
        return "%s %s" % (self.host_obj, self.model)