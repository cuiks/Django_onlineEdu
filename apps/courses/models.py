# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="course/ueditor/image/",
                          filePath="course/ueditor/file/", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    degree = models.CharField(max_length=5, verbose_name=u'课程难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')))
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(default='后端开发', max_length=20, verbose_name=u'课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name=u'课程标签')
    teacher = models.ForeignKey(Teacher, verbose_name=u'课程讲师', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    # 设置后台显示的标签title
    get_zj_nums.short_description = u'章节数'

    # 后天添加跳转
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://127.0.0.1:8000/courses/detail/{}/">跳转<a/>'.format(self.id))

    def get_learn_user(self):
        # 获取学习用户
        return self.usercourse_set.all()[:5]

    def get_zj(self):
        # 获取课程所有章节
        return self.lesson_set.all()


# 把课程中是轮播课程的单独展示
class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_video(self):
        # 根据章节获取video
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    url = models.CharField(max_length=100, default='', verbose_name=u'视频地址')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
