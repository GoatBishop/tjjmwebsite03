# Generated by Django 2.2.13 on 2020-10-23 08:56

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator('[\\u4E00-\\u9FA5]+', message='院校名请输入汉字,注意不要加空格！')], verbose_name='院校名称')),
                ('school_first_name', models.CharField(default='', max_length=30, verbose_name='院校首字母')),
                ('contacts', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('[\\u4E00-\\u9FA5]+', message='姓名请输入汉字,注意不要加空格！')], verbose_name='院校联系人')),
                ('school_class', models.CharField(default='大学', max_length=30, verbose_name='院校类型')),
                ('contacts_telephone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('1[3456789]\\d{9}', message='请输入正确格式的手机号码！')], verbose_name='手机号')),
                ('password', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('\\w{6,16}', message='请输入正确格式的密码！')], verbose_name='密码')),
                ('audit_status', models.CharField(default='待审核', max_length=20, verbose_name='审核状态')),
                ('number_team', models.PositiveIntegerField(default=20, verbose_name='名额数量')),
                ('admin_verification', models.CharField(default='否', max_length=10, verbose_name='管理员是否审核通过')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 10, 23, 8, 56, 44, 384293, tzinfo=utc), verbose_name='添加时间')),
            ],
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('1[3456789]\\d{9}', message='请输入正确格式的手机号码！')], verbose_name='手机号')),
                ('group', models.CharField(default='参赛队员', max_length=30, verbose_name='人员类型')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='指导教师姓名')),
                ('telephone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('1[3456789]\\d{9}', message='请输入正确格式的手机号码！')], verbose_name='手机号')),
                ('id_number', models.CharField(default='', max_length=30, verbose_name='身份证号')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 10, 23, 8, 56, 44, 385293, tzinfo=utc), verbose_name='添加时间')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor', to='backManage.College')),
            ],
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judge_username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('judge_name', models.CharField(default='', max_length=30, verbose_name='评委姓名')),
                ('password', models.CharField(default='000000', max_length=6, verbose_name='密码')),
                ('judge_type', models.CharField(default='普通评委', max_length=30, verbose_name='评委类型')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 10, 23, 8, 56, 44, 391293, tzinfo=utc), verbose_name='添加时间')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_name', models.CharField(max_length=30, verbose_name='成员姓名')),
                ('student_number', models.CharField(default='', max_length=30, verbose_name='学号')),
                ('telephone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('1[3456789]\\d{9}', message='请输入正确格式的手机号码！')], verbose_name='手机号')),
                ('id_number', models.CharField(default='', max_length=30, verbose_name='身份证号')),
                ('grade', models.CharField(default='大二', max_length=30, verbose_name='年级')),
                ('major', models.CharField(default='统计学', max_length=30, verbose_name='专业')),
                ('class_in_school', models.CharField(default='统计0班', max_length=30, verbose_name='班级')),
                ('is_captain', models.CharField(default='否', max_length=2, verbose_name='是否为队长')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 10, 23, 8, 56, 44, 386293, tzinfo=utc), verbose_name='添加时间')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='本科生组', max_length=30, verbose_name='组别')),
                ('work_group', models.CharField(default='大数据应用类', max_length=30, verbose_name='参赛项目类别')),
                ('game_type', models.CharField(default='复赛', max_length=30, verbose_name='赛程类型')),
                ('password', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('\\w{6,16}', message='请输入正确格式的密码！')], verbose_name='密码')),
                ('first_instru_telephone', models.CharField(default='', max_length=11, verbose_name='第一指导教师手机号')),
                ('tele_member2', models.CharField(default='00000', max_length=11, verbose_name='成员2手机号')),
                ('tele_member3', models.CharField(default='00000', max_length=11, verbose_name='成员3手机号')),
                ('work_id', models.CharField(max_length=20, unique=True, verbose_name='项目编号')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 10, 23, 8, 56, 44, 387293, tzinfo=utc), verbose_name='添加时间')),
                ('status', models.CharField(default='待完善信息', max_length=20, verbose_name='状态')),
                ('status_is_pass', models.CharField(default='未通过', max_length=20, verbose_name='是否通过')),
                ('status_is_submit', models.CharField(default='未报送', max_length=20, verbose_name='是否报送')),
                ('status_is_review', models.CharField(default='否', max_length=20, verbose_name='是否提交评分')),
                ('status_review_end', models.CharField(default='否', max_length=20, verbose_name='是否评分完毕')),
                ('instru', models.ManyToManyField(null=True, related_name='team', to='backManage.Instructor')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='backManage.College')),
                ('telephone', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='backManage.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 10, 23, 8, 56, 44, 389293, tzinfo=utc))),
                ('paper_word', models.FileField(null=True, upload_to='word', validators=[django.core.validators.FileExtensionValidator(['doc', 'docx'], message='文件必须为doc/docx格式')], verbose_name='作品word版')),
                ('paper_pdf', models.FileField(null=True, upload_to='pdf', validators=[django.core.validators.FileExtensionValidator(['pdf'], message='文件必须为pdf格式')], verbose_name='作品pdf版')),
                ('paper_cc', models.FileField(null=True, upload_to='cc', validators=[django.core.validators.FileExtensionValidator(['pdf'], message='查重报告必须为pdf格式')], verbose_name='查重报告pdf版')),
                ('paper_commit', models.FileField(null=True, upload_to='commit', validators=[django.core.validators.FileExtensionValidator(['pdf'], message='承诺书必须为pdf格式')], verbose_name='承诺书pdf版')),
                ('paper_sign_up', models.FileField(null=True, upload_to='sign_up', validators=[django.core.validators.FileExtensionValidator(['doc', 'docx'], message='报名表必须为doc/docx格式')], verbose_name='报名表word版')),
                ('paper_game_data', models.FileField(null=True, upload_to='game_data', validators=[django.core.validators.FileExtensionValidator(['zip', 'rar'], message='原始数据必须为zip/rar格式')], verbose_name='原始数据zip版')),
                ('status', models.CharField(default='未上传', max_length=20, verbose_name='状态')),
                ('work_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='work', to='backManage.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judge_score', models.PositiveIntegerField(default=0, verbose_name='得分')),
                ('judge_detail', models.CharField(default='', max_length=100, verbose_name='评价')),
                ('judge_is_review', models.CharField(default='否', max_length=2, verbose_name='评委是否提交评分')),
                ('judge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='backManage.Judge')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='backManage.Work')),
            ],
        ),
        migrations.AddField(
            model_name='judge',
            name='judge_works',
            field=models.ManyToManyField(null=True, related_name='judge', to='backManage.Work'),
        ),
    ]
