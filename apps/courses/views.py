from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.

class CourseListView(View):
    '''
    课程列表页
    '''

    def get(self, request):
        all_courses = Course.objects.order_by('-add_time')
        # 热门课程推荐
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 全局搜索框
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_courses = all_courses.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))

        # 筛选功能
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('-students')

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    '''课程详情页'''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 相关课程推荐
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag).exclude(id=course.id)[:1]
        else:
            relate_course = []

        has_fav_course = False
        has_fav_org = False
        # 判断是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    '''课程章节信息页'''

    def get(self, request, course_id):
        # 课程
        course = Course.objects.get(id=course_id)

        # 开始学习，数据库添加记录
        temp_user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not temp_user_course:
            temp_user_course = UserCourse(user=request.user, course=course)
            temp_user_course.save()

        # 资料下载
        course_files = CourseResource.objects.filter(course_id=course.id)
        # 课程讲师
        teacher = course.teacher
        ###学过改课的同学还学过###
        # 所有学过此课程的学生
        user_course = UserCourse.objects.filter(course_id=course.id)
        all_users = list(set([user_course.user.id for user_course in user_course]))
        # 这些学生学过的其他课程id
        all_user_course = UserCourse.objects.filter(user_id__in=all_users)
        all_course_ids = list(set([user_course.course.id for user_course in all_user_course]))
        # 根据id取出所有课程
        all_courses = Course.objects.filter(id__in=all_course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'course_files': course_files,
            'teacher': teacher,
            'all_courses': all_courses
        })


class VideoPlayView(LoginRequiredMixin, View):
    '''视频播放页面'''

    def get(self, request, video_id):
        # 课程
        video = Video.objects.get(id=video_id)
        course = video.lesson.course

        # 资料下载
        course_files = CourseResource.objects.filter(course_id=course.id)
        # 课程讲师
        teacher = course.teacher
        ###学过改课的同学还学过###
        # 所有学过此课程的学生
        user_course = UserCourse.objects.filter(course_id=course.id)
        all_users = list(set([user_course.user.id for user_course in user_course]))
        # 这些学生学过的其他课程id
        all_user_course = UserCourse.objects.filter(user_id__in=all_users)
        all_course_ids = list(set([user_course.course.id for user_course in all_user_course]))
        # 根据id取出所有课程
        all_courses = Course.objects.filter(id__in=all_course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-play.html', {
            'course': course,
            'course_files': course_files,
            'teacher': teacher,
            'all_courses': all_courses,
            'video':video
        })


class CourseCommentView(LoginRequiredMixin, View):
    '''课程评论页'''

    def get(self, request, course_id):
        # 课程
        course = Course.objects.get(id=course_id)

        # 开始学习，数据库添加记录
        temp_user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not temp_user_course:
            temp_user_course = UserCourse(user=request.user, course=course)
            temp_user_course.save()

        # 资料下载
        course_files = CourseResource.objects.filter(course_id=course.id)
        # 课程讲师
        teacher = course.teacher
        # 课程评论
        course_comments = CourseComments.objects.filter(course_id=course_id)
        ###学过改课的同学还学过###
        # 所有学过此课程的学生
        user_course = UserCourse.objects.filter(course_id=course.id)
        all_users = list(set([user_course.user.id for user_course in user_course]))
        # 这些学生学过的其他课程id
        all_user_course = UserCourse.objects.filter(user_id__in=all_users)
        all_course_ids = list(set([user_course.course.id for user_course in all_user_course]))
        # 根据id取出所有课程
        all_courses = Course.objects.filter(id__in=all_course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-comment.html', {
            'course': course,
            'course_files': course_files,
            'teacher': teacher,
            'course_comments': course_comments,
            'all_courses': all_courses
        })


class AddCommentView(View):
    '''添加评论'''

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course = Course.objects.get(id=course_id)
            course_comment = CourseComments()
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')
