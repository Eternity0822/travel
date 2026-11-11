
from django.utils import timezone
from django.db import models

# 创建用户数据库模型
class UserInfo(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名')  # 用户名
    password = models.CharField(max_length=40, verbose_name='密码')  # 密码
    uemail = models.EmailField(max_length=40, verbose_name='邮箱')  # 邮箱
    uaddress = models.CharField(max_length=30, verbose_name='地址', default='')  # 地址
    uyoubian = models.CharField(max_length=30, verbose_name='邮编', default='')  # 邮编
    uphone = models.CharField(max_length=30, verbose_name='电话号码', default='')  # 电话号码
    avatar = models.CharField(max_length=255, verbose_name='头像', default='')  # 头像的URL地址
    created_at = models.DateTimeField(default=timezone.now())  # 创建时间

    def __str__(self):
        return self.username
    
    # 后台管理页面显示
    class Meta:
        verbose_name_plural = '用户管理'
