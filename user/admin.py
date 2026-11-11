from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from user.models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = (
        'username',
        'uemail',
        'uphone',
        'uaddress',
        'created_at',
        'show_avatar'
    )
    # 可以点击进入编辑页面的字段
    list_display_links = ('username', 'uemail')
    # 可筛选的字段
    list_filter = ('created_at',)
    # 可搜索的字段 
    search_fields = ('username', 'uemail', 'uphone')
    # 分页设置
    list_per_page = 20\
    # 按时间创建排序
    ordering = ('-created_at',)
    # 编辑页面的字段分组布局
    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'password', 'uemail', 'avatar')
        }),
        ('联系信息', {
            'fields': ('uphone', 'uaddress', 'uyoubian')
        }),
        ('其他信息', {
            'fields': ('created_at',)
        }),
    )

    # 自定义方法显示头像
    def show_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;border-radius: 50%;" />', 
                obj.avatar.url if hasattr(obj.avatar, 'url') else obj.avatar
            )
        return format_html('<span style="color: gray;">无头像</span>')
    
    show_avatar.short_description = '头像预览'
    show_avatar.admin_order_field = 'avatar'  # 允许通过头像字段排序

# 注册模型和自定义的Admin类
admin.site.register(UserInfo, UserInfoAdmin)