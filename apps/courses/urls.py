# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView,AddCommentView

urlpatterns = [
    # 课程列表页
    url('^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url('^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程章节页
    url('^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论页
    url('^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    # 对课程添加评论
    url('^add_comment/$', AddCommentView.as_view(), name='add_comment'),
]
