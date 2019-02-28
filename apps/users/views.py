# _*_ encoding:utf-8 _*_
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response

from courses.models import Course
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm, UploadImageForm, UserInfoForm
from utils.email_send import send_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher


# Create your views here.

class CustomBackend(ModelBackend):
    '''用户登录逻辑，重写authenticate方法'''

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# def user_login(request):
#     '''自定义登录逻辑'''
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})

class LoginView(View):
    '''通过类和继承实现自定义登录逻辑'''

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogOutView(View):
    '''退出登录'''

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    '''注册View'''

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'msg': '该用户已注册', 'register_form': register_form})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()
            send_email(username, 'register')
            print('邮件发送')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    '''用户激活'''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html', {'msg': '激活成功'})
        else:
            return render(request, 'active_fail.html')


class ForgetPwdView(View):
    '''忘记密码'''

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    '''重置密码页面'''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})

        else:
            return render(request, 'active_fail.html')


class ModifyPwdForm(View):
    '''重置密码逻辑'''

    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd2 != pwd1:
                return render(request, 'password_reset.html', {'email': email, 'msg': '两次输入密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    '''用户个人信息'''

    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    '''用户上传头像'''

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            status = image_form.save()
            print(status)
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdForm(View):
    '''用户个人中心修改密码'''

    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd2 != pwd1:
                return HttpResponse('{"status":"fail","msg":"密码不一致！"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(View):
    '''修改邮箱发送验证码'''

    def get(self, request):
        email = request.GET.get('email')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已注册"}', content_type='application/json')
        send_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(View):
    '''修改邮箱'''

    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        if EmailVerifyRecord.objects.filter(email=email, code=code):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    '''我的课程页面'''

    def get(self, request):
        user = request.user
        all_courses = UserCourse.objects.filter(user=user)
        return render(request, 'usercenter-mycourse.html', {
            'all_courses': all_courses
        })


class UserFavOrgView(LoginRequiredMixin, View):
    '''个人中心课程机构收藏'''

    def get(self, request):
        all_org_id = UserFavorite.objects.filter(user_id=request.user.id, fav_type=2)
        all_org_ids = [item.fav_id for item in all_org_id]
        all_orgs = CourseOrg.objects.filter(id__in=all_org_ids)
        return render(request, 'usercenter-fav-org.html', {
            'all_orgs': all_orgs
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    '''个人中心讲师收藏'''

    def get(self, request):
        all_teacher_id = UserFavorite.objects.filter(user_id=request.user.id, fav_type=3)
        all_teacher_ids = [item.fav_id for item in all_teacher_id]
        all_teachers = Teacher.objects.filter(id__in=all_teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'all_teachers': all_teachers
        })


class UserFavCourseView(LoginRequiredMixin, View):
    '''个人中心课程收藏'''

    def get(self, request):
        all_course_id = UserFavorite.objects.filter(user_id=request.user.id, fav_type=1)
        all_course_ids = [item.fav_id for item in all_course_id]
        all_courses = Course.objects.filter(id__in=all_course_ids)
        return render(request, 'usercenter-fav-course.html', {
            'all_courses': all_courses
        })


class UserMessageView(LoginRequiredMixin, View):
    '''个人中心，我的消息'''

    def get(self, request):
        all_messages = UserMessage.objects.filter(Q(user=request.user.id) | Q(user=0))
        for item_message in all_messages:
            item_message.has_read = True
            item_message.save()
        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 3, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'all_messages': messages
        })


class IndexView(View):
    '''首页view'''
    def get(self, request):
        all_banner = Banner.objects.all()[:5]
        banner_courses = Course.objects.filter(is_banner=True)
        courses = Course.objects.filter(is_banner=False)[:6]
        orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banner':all_banner,
            'banner_courses':banner_courses,
            'courses':courses,
            'orgs':orgs
        })


def page_not_found(request):
    '''404页面'''
    response = render_to_response('404.html')
    response.status_code = 404
    return response



def server_error(request):
    '''500页面'''
    response = render_to_response('500.html')
    response.status_code = 500
    return response
