# -*- coding: utf-8 -*-
import xadmin
from users.models import EmailVerifyRecord, Banner
from xadmin import views


class BaseSetting(object):
    # 使用主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 设置页头
    site_title = '慕学后台管理系统'
    # 设置页脚
    site_footer = '慕学在线网'
    # 折叠目录
    menu_style = 'accordion'



class EmailVerifyRecordAdmin(object):
    # 设置默认显示条目及顺序
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 添加搜索框
    search_fields = ['code', 'email', 'send_type']
    # 添加过滤器
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
