# _*_ encoding:utf-8 _*_
"""MxOnlineProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from users.views import LoginView, LogOutView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdForm
from users.views import IndexView
from organization.views import OrgView
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogOutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url('^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url('^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url('^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url('^modify_pwd/$', ModifyPwdForm.as_view(), name='modify_pwd'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 配置用户上传文件的访问处理
    url('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 配置静态文件的访问处理
    # url('^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # 课程列表页url配置
    url(r'^courses/', include('courses.urls', namespace='courses')),

    # 个人中心url配置
    url(r'^users/', include('users.urls', namespace='users')),
    # ueditor
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

# 配置全局404页面
handler404 = 'users.views.page_not_found'

# 配置全局500页面
handler500 = 'users.views.server_error'
