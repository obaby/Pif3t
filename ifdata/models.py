from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import User


class IFTTTType(models.Model):
    create = models.DateTimeField(default=timezone.now, help_text='创建时间')
    update = models.DateTimeField(auto_now=True, help_text='修改时间')
    name = models.CharField(blank=True, null=True, max_length=64, help_text='名称')
    describe = models.TextField(blank=True, null=True, max_length=4095, help_text='说明')
    type_id = models.IntegerField(default=1, help_text='类型ID')

    def __unicode__(self):
        return '%(name)s [%(count)s]' % {"name": str(self.name), "count": self.id}

    def __str__(self):
        return '%(name)s [%(count)s]' % {"name": str(self.name) , "count": self.id}

    class Meta:
        verbose_name = 'IFTTT类型'
        verbose_name_plural = 'IFTTT类型'


class ThatAction(models.Model):
    create = models.DateTimeField(default=timezone.now, help_text='创建时间')
    update = models.DateTimeField(auto_now=True, help_text='修改时间')
    action_type = models.IntegerField(default=0, help_text='动作类型')
    http_url = models.CharField(blank=True, null=True, max_length=1024, help_text='Http请求URL')
    http_header = models.CharField(blank=True, null=True, max_length=1024, help_text='Http请求Header')
    http_body = models.CharField(blank=True, null=True, max_length=1024, help_text='Http请求Body')
    http_method = models.CharField(default='get', max_length=8, help_text='Http请求方法')

    name = models.CharField(blank=True, null=True, max_length=64, help_text='名称')
    describe = models.TextField(blank=True, null=True, max_length=4095, help_text='说明')
    response_text = models.TextField(blank=True, null=True, help_text='动作执行反馈文本 随机文本反馈根据换行分割')

    def __unicode__(self):
        return '%(name)s [%(count)s]' % {"name": str(self.name), "count": self.id}

    def __str__(self):
        return '%(name)s [%(count)s]' % {"name": str(self.name) , "count": self.id}

    class Meta:
        verbose_name = 'ThatAction'
        verbose_name_plural = 'ThatAction'


class IfThis(models.Model):
    create = models.DateTimeField(default=timezone.now, help_text='创建时间')
    update = models.DateTimeField(auto_now=True, help_text='修改时间')
    name = models.CharField(blank=True, null=True, max_length=64, help_text='名称')
    describe = models.TextField(blank=True, null=True, max_length=4095, help_text='说明')
    condition_type = models.CharField(default='has', max_length=16, help_text='关键词匹配方法')
    key_words = models.CharField(blank=True, null=True, max_length=128, help_text='关键词列表 | 分割')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, help_text='父条件')
    that_action = models.ManyToManyField(ThatAction, blank=True, help_text='动作行为')
    enable = models.BooleanField(default=True, help_text='是否激活')
    no_action_response_text = models.TextField(blank=True, null=True, help_text='未绑定动作反馈文本 随机文本反馈根据换行分割')
    if_type = models.ForeignKey(IFTTTType, blank=True, null=True, on_delete=models.SET_NULL, help_text='条件类型')

    def __unicode__(self):
        return '%(name)s [%(count)s]' % {"name": str(self.name), "count": self.id}

    def __str__(self):
        return '%(name)s [%(count)s]' % {"name": str(self.name) , "count": self.id}

    class Meta:
        verbose_name = 'IfThis'
        verbose_name_plural = 'IfThis'