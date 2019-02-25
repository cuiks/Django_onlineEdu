# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from organization.views import OrgView, AddUserAskView

urlpatterns = [
    # 课程机构列表页
    url('^list/$', OrgView.as_view(), name='org_list'),
    # 用户咨询
    url('^add_ask/$', AddUserAskView.as_view(), name='add_ask')
]
