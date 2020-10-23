from django.db import models
from django.utils import timezone
from django.core import validators


class College(models.Model):
    school = models.CharField('院校名称', max_length = 30,
                              validators=[validators.RegexValidator(r"[\u4E00-\u9FA5]+",message='院校名请输入汉字,注意不要加空格！')],
                              unique=True)
    school_first_name = models.CharField('院校首字母', max_length = 30,
                                         default = "")
    contacts = models.CharField('院校联系人', max_length = 30,
                                validators=[validators.RegexValidator(r"[\u4E00-\u9FA5]+",message='姓名请输入汉字,注意不要加空格！')])
    school_class = models.CharField('院校类型', max_length = 30,
                                    default = "大学")
    contacts_telephone = models.CharField("手机号", max_length = 11,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')],
                                          unique=True)
    password = models.CharField('密码', max_length = 16,
                                validators=[validators.RegexValidator(r"\w{6,16}", message = '请输入正确格式的密码！')])
    audit_status = models.CharField('审核状态', max_length = 20,
                                    default = "待审核")
    number_team = models.PositiveIntegerField("名额数量", default = 20)
    
    admin_verification = models.CharField('管理员是否审核通过', max_length = 10,
                                    default = "否")
    
    add_time = models.DateTimeField("添加时间", default = timezone.now())
    
    def __str__(self):
        return self.school

class Instructor(models.Model):
    name = models.CharField('指导教师姓名', max_length = 30)
    telephone = models.CharField("手机号", max_length = 11,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')],
                                          unique=True)
#    password = models.CharField('密码', max_length = 16,
#                                validators=[validators.RegexValidator(r"\w{6,16}", message = '请输入正确格式的密码！')])
    id_number = models.CharField("身份证号", max_length = 30, default = "")
    school = models.ForeignKey("College", on_delete = models.CASCADE,
                               related_name = "instructor")
    add_time = models.DateTimeField("添加时间", default = timezone.now())
    
    def __str__(self):
        return self.name

class Member(models.Model):
    member_name = models.CharField('成员姓名', max_length = 30)
    student_number = models.CharField('学号', max_length = 30, default = "")
    telephone = models.CharField("手机号", max_length = 11,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')],
                                          unique=True)
    id_number = models.CharField("身份证号", max_length = 30, default = "")
    grade = models.CharField('年级', max_length = 30, default = "大二")
    major = models.CharField('专业', max_length = 30, default = "统计学")
    class_in_school = models.CharField('班级', max_length = 30, default = "统计0班")
    is_captain = models.CharField('是否为队长', max_length = 2, default = "否")
    add_time = models.DateTimeField("添加时间", default = timezone.now())
    
    def __str__(self):
        return self.telephone

class Team(models.Model):
    school = models.ForeignKey("College", on_delete = models.CASCADE, related_name = "team")
    group = models.CharField('组别', max_length = 30, default = "本科生组")
    work_group = models.CharField('参赛项目类别', max_length = 30, default = "大数据应用类")
    game_type = models.CharField('赛程类型', max_length = 30, default = "复赛")

#   captain = models.CharField('团队长姓名', max_length = 30)
    telephone = models.OneToOneField('Member', on_delete = models.CASCADE,
                                             related_name = "team")
    
    password = models.CharField('密码', max_length = 16,
                                validators=[validators.RegexValidator(r"\w{6,16}", message = '请输入正确格式的密码！')])
    
    instru = models.ManyToManyField("Instructor", related_name = "team", null = True)
    first_instru_telephone = models.CharField('第一指导教师手机号', max_length = 11, default = "")
    tele_member2 = models.CharField("成员2手机号", max_length = 11, default = "00000")
    tele_member3 = models.CharField("成员3手机号", max_length = 11, default = "00000")
    work_id = models.CharField("项目编号", max_length = 20, unique = True)
    add_time = models.DateTimeField("添加时间", default = timezone.now())
    status = models.CharField('状态', max_length = 20, default = "待完善信息")
    #待完善信息-> 待审核 -> 通过/未通过 -> 报送/退回
    status_is_pass = models.CharField('是否通过', max_length = 20, default = "未通过")
    #团队信息是否通过
    #通过/未通过
    status_is_submit = models.CharField('是否报送', max_length = 20, default = "未报送")
    #被院校and后台退回这里不显示退回,如果作品被报送,那么这里就会显示报送,如果后台退回,这里则显示退回
    #团队是否被学校报送
    #未报送/报送/退回
    status_is_review = models.CharField('是否提交评分', max_length = 20, default = "否")
    #是/否
    status_review_end = models.CharField('是否评分完毕', max_length = 20, default = "否")
    #是/否
    
    def __str__(self):
        return  self.work_id

#========表关联分界线======

class Work(models.Model):
    work_id = models.OneToOneField('Team', on_delete = models.CASCADE,
                                             related_name = "work")
    add_time = models.DateTimeField(default = timezone.now())
    paper_word = models.FileField("作品word版", upload_to = "word", null = True, 
                             validators = [validators.FileExtensionValidator(['doc', 'docx'],
                                                                           message = "文件必须为doc/docx格式")])
    
    paper_pdf = models.FileField("作品pdf版", upload_to = "pdf", null = True,
                             validators = [validators.FileExtensionValidator(['pdf'],
                                                                           message = "文件必须为pdf格式")])
    
    paper_cc = models.FileField("查重报告pdf版", upload_to = "cc", null = True,
                             validators = [validators.FileExtensionValidator(['pdf'],
                                                                           message = "查重报告必须为pdf格式")])
    paper_commit = models.FileField("承诺书pdf版", upload_to = "commit", null = True,
                             validators = [validators.FileExtensionValidator(['pdf'],
                                                                           message = "承诺书必须为pdf格式")])

    paper_sign_up = models.FileField("报名表word版", upload_to = "sign_up", null = True,
                             validators = [validators.FileExtensionValidator(['doc', 'docx'],
                                                                           message = "报名表必须为doc/docx格式")])
    paper_game_data = models.FileField("原始数据zip版", upload_to = "game_data", null = True,
                             validators = [validators.FileExtensionValidator(['zip', 'rar'],
                                                                           message = "原始数据必须为zip/rar格式")])

    
    status = models.CharField('状态', max_length = 20, default="未上传")
        
    def __str__(self):
        return  self.work_id

class Judge(models.Model):
    judge_username = models.CharField('用户名', max_length = 20, unique = True)
    judge_name = models.CharField('评委姓名', max_length = 30, default = "")
    password = models.CharField('密码', max_length = 6, default = "000000")
    judge_type = models.CharField('评委类型', max_length = 30, default = "普通评委")
    judge_works = models.ManyToManyField("Work", related_name = "judge", null = True)
    add_time = models.DateTimeField("添加时间", default = timezone.now())
    def __str__(self):
        return  self.judge_username

class Score(models.Model):
    work = models.ForeignKey('Work', on_delete = models.CASCADE, related_name = "score")
    judge = models.ForeignKey('Judge', on_delete = models.CASCADE, related_name = "score")
    
    judge_score = models.PositiveIntegerField("得分", default = 0)
    judge_detail = models.CharField('评价', max_length = 100, default="")
    judge_is_review = models.CharField('评委是否提交评分', max_length = 2, default="否")
    def __str__(self):
        return  "评分为" + str(self.judge_score)
    

class Directory(models.Model):
    telephone = models.CharField("手机号", max_length = 11,
                                          validators=[validators.RegexValidator("1[3456789]\d{9}",message='请输入正确格式的手机号码！')],
                                          unique=True)
    group = models.CharField('人员类型', max_length = 30, default = "参赛队员")
    #参赛队员/院校负责人
    def __str__(self):
        return  self.telephone

