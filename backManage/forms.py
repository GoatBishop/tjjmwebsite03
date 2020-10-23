# -*- coding: utf-8 -*-
from django import forms
from django.core import validators
from .models import Team, Member, Instructor, College, Work


def get_errors(modeling):
    #获取错误函数
    errors = modeling.errors.get_json_data()
    new_errors = {}
    for key,message_dicts in errors.items():
        messages = []
        for message in message_dicts:
            messages.append(message['message'])
        new_errors[key] = messages
    return new_errors


#College
class CollegeForm(forms.ModelForm):  
    class Meta:
        model = College
        fields = ['school', "contacts",
                  "contacts_telephone", "password"]

#Instructor
class InstructorForm(forms.ModelForm):  
    class Meta:
        model = Instructor
        fields = ['name', 'telephone']

class CaptainForm(forms.Form):
#    member_name = forms.CharField(max_length = 30,
#                              validators=[validators.RegexValidator(r"[\u4E00-\u9FA5]+",message='请输入汉字！')])
    grade = forms.CharField(max_length = 30,
                              validators=[validators.RegexValidator(r"大一|大二|大三|大四|研一|研二|研三",message='请输入下拉框里的内容!')])

class MemberForm(forms.Form):
    member_name = forms.CharField(max_length = 30,
                              validators=[validators.RegexValidator(r"[\u4E00-\u9FA5]+",message='请输入汉字！')])
    grade = forms.CharField(max_length = 30,
                              validators=[validators.RegexValidator(r"大一|大二|大三|大四|研一|研二|研三",message='请输入下拉框里的内容!')])
    telephone = forms.CharField(max_length = 11,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')])


class TeamForm(forms.Form):
    password = forms.CharField(max_length = 16,
                                validators=[validators.RegexValidator(r"\w{6,16}", message = '请输入正确格式的密码！')])
    password2 = forms.CharField(max_length = 16,
                                validators=[validators.RegexValidator(r"\w{6,16}", message = '请输入正确格式的密码！')])
    captain = forms.CharField(max_length = 30,
                              validators=[validators.RegexValidator(r"[\u4E00-\u9FA5]+",message='请输入汉字,注意不要加空格！')])
    #[\u4E00-\u9FA5]+
    telephone = forms.CharField(max_length = 11,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('两个密码不一致！')

class TeamChangePswForm(forms.Form):
    #用于修改密码的Team表单
    password = forms.CharField(max_length = 16,
                                validators=[validators.RegexValidator(r"\w{6,16}", message = '请输入正确格式的密码！')])
    password2 = forms.CharField(max_length = 16,
                                validators=[validators.RegexValidator(r"\w{6,16}", message = '请输入正确格式的密码！')])
    telephone = forms.CharField(max_length = 11,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('两个密码不一致！')

class TeamChangeInfoForm(forms.Form):
    group = forms.CharField(max_length = 30,
                              validators=[validators.RegexValidator(r"研究生组|本科生组",message='请输入下拉框里的内容!')])
    work_group =  forms.CharField(max_length = 30,
                              validators=[validators.RegexValidator(r"统计建模类|大数据应用类|市场调查分析类|生物医学类",message='请输入下拉框里的内容!')])

    first_instru_name = forms.CharField(max_length = 30, required = False,
                                        validators=[validators.RegexValidator(r"[\u4E00-\u9FA5]+",message='请输入汉字,注意不要加空格！')])
    first_instru_telephone = forms.CharField(max_length = 11, required = False,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')])
    
    second_instru_name = forms.CharField(max_length = 30, required = False,
                              validators=[validators.RegexValidator(r"[\u4E00-\u9FA5]+",message='请输入汉字,注意不要加空格！')])
    
    second_instru_telephone = forms.CharField(max_length = 11, required = False,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')])

class TeamFindForm(forms.Form):
    group = forms.CharField(max_length = 30, required = False, 
                              validators=[validators.RegexValidator(r"研究生组|本科生组",message='请输入下拉框里的内容!')])
    work_group =  forms.CharField(max_length = 30, required = False, 
                              validators=[validators.RegexValidator(r"统计建模类|大数据应用类|市场调查分析类|生物医学类",message='请输入下拉框里的内容!')])

class WorkForm(forms.Form):
    paper_word = forms.FileField(required = False, 
                                 validators = [validators.FileExtensionValidator(['doc', 'docx'], message = "文件必须为doc/docx格式")])
            
    paper_pdf = forms.FileField(required = False, 
                                validators = [validators.FileExtensionValidator(['pdf'], message = "文件必须为pdf格式")])
    paper_cc = forms.FileField(required = False, 
                               validators = [validators.FileExtensionValidator(['pdf'], message = "文件必须为pdf格式")])
    paper_commit = forms.FileField(required = False, 
                                 validators = [validators.FileExtensionValidator(['pdf'], message = "文件必须为pdf格式")])
            
    paper_sign_up = forms.FileField(required = False, 
                                validators = [validators.FileExtensionValidator(['doc', 'docx'], message = "文件必须为doc/docx格式")])
    paper_game_data = forms.FileField(required = False, 
                               validators = [validators.FileExtensionValidator(['zip', 'rar'], message = "文件必须为zip/rar格式")])

#    class Meta:
#        model = Work
#        fields = ['paper_word', 'paper_pdf']

class WorkScoreForm(forms.Form):
    score = forms.CharField(validators=[validators.RegexValidator(r"[0-9]|[1-9]\d|100",message='请输入0~100之内的整数！')])
    
    
class JudgeForm(forms.Form):
    judge_username = forms.CharField(max_length = 20)
    password = forms.CharField(validators=[validators.RegexValidator(r"r\w{5}", message = '请输入格式为[小写字母r + 5位数字]的6位密码,！')])
    judge_type = forms.CharField(max_length = 30,
                              validators=[validators.RegexValidator(r"普通评委|非普通评委",message='请输入下拉框里的内容!')])