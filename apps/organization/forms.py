# -*- coding: utf-8 -*-
import re

from django.forms import ModelForm, forms
from operation.models import UserAsk


class UserAskForm(ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''
        验证手机号码是否合法
        '''
        mobile = self.cleaned_data['mobile']
        pattern_mobile = r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$'
        p = re.compile(pattern_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code='invalid_mobil')
