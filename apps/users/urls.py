# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdForm, SendEmailCodeView, UpdateEmailView
from .views import UserInfoView, MyCourseView, UserFavOrgView, UserFavTeacherView, UserFavCourseView,UserMessageView

urlpatterns = [
    # 课程机构列表页
    url('^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url('^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url('^update/pwd/$', UpdatePwdForm.as_view(), name='update_pwd'),
    # 修改邮箱发送验证码
    url('^send_code/$', SendEmailCodeView.as_view(), name='send_code'),
    # 修改邮箱
    url('^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    url('^my_course/$', MyCourseView.as_view(), name='my_course'),
    # 课程机构收藏
    url('^fav_org/$', UserFavOrgView.as_view(), name='fav_org'),
    # 课程讲师收藏
    url('^fav_teacher/$', UserFavTeacherView.as_view(), name='fav_teacher'),
    # 课程课程收藏
    url('^fav_course/$', UserFavCourseView.as_view(), name='fav_course'),
    # 我的消息
    url('^message/$', UserMessageView.as_view(), name='message'),

]
