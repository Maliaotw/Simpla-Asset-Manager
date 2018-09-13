from django.db import models

# Create your models here.


class Host(models.Model):
    '''
    主機資產表
    '''

    host_type_choice = (
        (1, '工作站'),
        (2, '值班電腦'),
        (3, '培訓電腦'),
        (4, '備用電腦'),
        (5, '汰換機'),
        (6, '測試機'),
    )

    asset = models.OneToOneField('asset.Asset',null=True,blank=True)
    ops_owner = models.ForeignKey('asset.UserProfile',verbose_name="運維負責人",null=True, blank=True)
    location = models.ForeignKey('asset.Location', verbose_name='位置', null=True, blank=True)

    host_type_id = models.IntegerField(choices=host_type_choice, default=2)

    number = models.IntegerField(verbose_name="編號")
    sn = models.CharField('SN序號', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='製造商', max_length=64, null=True, blank=True)
    model = models.CharField('型號', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('IP', null=True, blank=True)

    os_platform = models.CharField('系統', max_length=16, null=True, blank=True)
    os_version = models.CharField('系統版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('邏輯處理器', null=True, blank=True)
    cpu_physical_count = models.IntegerField('處理器內核', null=True, blank=True)
    cpu_model = models.CharField('處理器型號', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "主機資產表"


    def __str__(self):
        return "PC-%03d %s" % (self.number,self.manage_ip)


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