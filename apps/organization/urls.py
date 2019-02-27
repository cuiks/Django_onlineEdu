# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, TeacherDetailView
from organization.views import OrgDescView, OrgTeacherView, AddFavView, TeacherListView

urlpatterns = [
    # 课程机构列表页
    url('^list/$', OrgView.as_view(), name='org_list'),
    # 用户咨询
    url('^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    # 机构首页
    url('^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    # 机构课程列表页
    url('^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='course'),
    # 机构介绍
    url('^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='desc'),
    # 机构教师
    url('^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    # 机构收藏
    url('^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 课程讲师列表
    url('^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    # 课程讲师详情
    url('^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail')
]
