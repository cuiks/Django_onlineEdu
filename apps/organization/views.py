# -*- coding: utf-8 -*-
from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from django.views.generic import View
from .models import CourseOrg, CityDict


class OrgView(View):
    '''课程机构列表'''

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        # 城市
        all_citys = CityDict.objects.all()

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 培训机构类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category
        })
