from django.shortcuts import render
from backManage import models
from backManage import forms
from django.http import HttpResponse,Http404
from django.shortcuts import redirect,reverse
import random
import time
# Create your views here.


def work_id_random(id_length = 2):
    #团队作品编号随机数生成器
    t = str(int(time.time()))
    work_id = "tjjm" + t
    num = ["5", "6", "7", "8", "9"]
    for item in range(id_length):
        work_id += random.choice(num)
    return work_id


def mylogin(request):
    if request.method == 'GET':
        print("teamManage: 我是mylogin的GET")
        telephone = request.COOKIES.get('telephone', '')
        return render(request, 'login-team.html', locals())
    elif request.method == 'POST':
        # 获取表单的数据
        print("teamManage: 我是mylogin的POST")
        telephone = request.POST.get('telephone', '')
        password = request.POST.get('password', '')
        print(telephone, "--", password)
#        # 验证用户名，密码是否正确
        try:
            print("我进入mylogin的try里来了")
            captain = models.Member.objects.get(telephone = telephone)
            user = models.Team.objects.get(telephone = captain,
                                           password = password)
            print(user)
            print("我存在数据库中")
            print(captain, "--", user)
            print("===我输出了===")
            # 在当前连接的Session中记录当前用户的信息
            request.session['userinfo'] = {
                "work_id": user.work_id,
                'telephone': telephone
            }
        except:
            #登录失败
            print("我登录失败了")
            return render(request, 'login-team.html', locals())
        # 处理COOKIES
        print("我要跳转到login-team.html")
        resp = redirect(reverse('team:teammain'))
        resp.set_cookie('telephone', telephone, 5*24*60*60)
        print("我已经设置了cookie")
        return resp

def mylogout(request):
    if 'userinfo' in request.session:
        del request.session['userinfo']
        print("我输出了")
    return redirect(reverse('team:tlogin')) 

def myregister(request):
    if request.method == 'GET':
        schools = models.College.objects.filter(admin_verification = "是")
        school_list = []
        for s in  schools:
            if s.school not in school_list:
                school_list.append(s.school)
        return render(request, 'team-reg.html', locals())
    elif request.method == 'POST':
        
        teamForm = forms.TeamForm(request.POST, request.FILES)
        if teamForm.is_valid():
            captain = teamForm.cleaned_data.get("captain")
            telephone = teamForm.cleaned_data.get("telephone")
            password = teamForm.cleaned_data.get("password")
            school_clean = request.POST.get('school', '')
            work_id = work_id_random()
            
            print("学校是：", school_clean)
            school = models.College.objects.get(school = school_clean)
            
            try:
                tele = models.Directory.objects.get(telephone = telephone)
                return HttpResponse("<h1>该号码已被注册!</h1>")
            except:
                try:
                    captain_user = models.Member.objects.create(member_name = captain,
                                                                telephone = telephone,
                                                                is_captain = "是")
                    user = models.Team.objects.create(school = school,
                                                       telephone = captain_user,
                                                       password = password,
                                                       work_id = work_id)
                    work = models.Work.objects.create(work_id = user)
                    tele = models.Directory.objects.create(telephone = telephone)
                except Exception as e:
                    print(e)
                    return HttpResponse("<div>注册失败, 该手机号可能已被注册！  <a href='/team/register/'>点击跳转到注册界面</a></div> \
                                        <br> <div>实在注册不成功, 可以进入人工服务通道, VX:gy1033794241</div> \
                                        <br> <div>服务时间:7:30 - 21:30 </div> \
                                        <br> <div>不常在线,看到回复,谢谢。 </div>")

            return HttpResponse("<h1>注册成功！</h1>")
        else:
            file_error = forms.get_errors(teamForm)
            telephone = request.POST.get('telephone', '')
            captain = request.POST.get('captain', '')
            
            schools = models.College.objects.all()
            school_list = []
            for s in  schools:
                if s.school not in school_list:
                    school_list.append(s.school)
                    
            print(teamForm.errors.get_json_data())
            print("我是: ", captain, "电话为: ", telephone)
            return render(request, 'team-reg.html', locals())
        
def repsw(request):
    if request.method == 'GET':
        return render(request, 'team-psw-forget.html', locals())
    elif request.method == 'POST':
        # 获取表单的数据
        telephone = request.POST.get('telephone', '')
#        password = request.POST.get('password', '')
#        password2 = request.POST.get('password2', '')
#        # 验证用户名，密码是否正确
#        if password != password2:
#            password2_error = "两次密码不一致"
#            return render(request, 'team-psw-forget.html', locals())
        try:
            captain_user = models.Member.objects.get(telephone = telephone,
                                             is_captain = "是")
            user = captain_user.team
            print(user)
            # 在当前连接的Session中记录当前用户的信息
        except:
            #手机验证失败
            user_error = "没有当前手机号"
            return render(request, 'team-psw-forget.html', locals())
        
        teamForm = forms.TeamChangePswForm(request.POST)
        if teamForm.is_valid():
            password = teamForm.cleaned_data.get("password")
            user.password = password
            user.save()
            return HttpResponse("<h1>修改密码成功！</h1>")        
        else:
            file_error = forms.get_errors(teamForm)
            telephone = request.POST.get('telephone', '')
            print(teamForm.errors.get_json_data())
            print("我是的电话为: ", telephone)
            return render(request, 'team-psw-forget.html', locals())


def team_index(request):
    session_team = request.session.get('userinfo', '')
    if session_team:
        print(session_team)
        #contacts_telephone
        telephone = session_team['telephone']
        user = models.Member.objects.get(telephone = telephone)
        member_name = user.member_name
        return render(request, "index-team.html", locals())
    else:
        print("我没有session")
        return redirect(reverse('team:tlogin'))

def team_part_info_team(request):
    ftele = ""
    stele = ""
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team
    school = team.school
    instructors = team.instru.all()
    print(instructors)
    if instructors:
        for instructor in instructors:
            if instructor.telephone == team.first_instru_telephone:
                first_instru_name = instructor.name
                first_instru_telephone = instructor.telephone
                
                #====
                ftele = first_instru_telephone
            else:
                second_instru_name = instructor.name
                second_instru_telephone = instructor.telephone
                stele = second_instru_telephone
    else:
        print("我没有instructor")
        first_instru_name = ""
        first_instru_telephone = ""
        second_instru_name = ""
        second_instru_telephone = ""
    
    if team.tele_member2 == "00000":
        pass
    else:
        member2 = models.Member.objects.get(telephone = team.tele_member2)
    
    if team.tele_member3 == "00000":
        pass
    else:
        member3 = models.Member.objects.get(telephone = team.tele_member3)
        
    schools = models.College.objects.all()
    school_list = []
    
    for s in  schools:
        if s.school not in school_list:
            school_list.append(s.school)
            
    if request.method == "GET":
        if ((team.status == "待完善信息") | (team.status == "退回") | (team.status == "未通过")):
            return render(request, 'info-team.html', locals())
        else:
            return redirect(reverse("team:savesubmit"))
    elif request.method == 'POST':
        teamInfoForm = forms.TeamChangeInfoForm(request.POST)
        if teamInfoForm.is_valid():
            group = teamInfoForm.cleaned_data.get("group")
            work_group = teamInfoForm.cleaned_data.get("work_group")
            team.group = group
            team.work_group = work_group
            team.save()
            
            first_instru_name = teamInfoForm.cleaned_data.get("first_instru_name", "")
            first_instru_telephone = teamInfoForm.cleaned_data.get("first_instru_telephone", "")
            second_instru_name = teamInfoForm.cleaned_data.get("second_instru_name", "")
            second_instru_telephone = teamInfoForm.cleaned_data.get("second_instru_telephone", "")
            
            #========save========
            
            
#            if ((first_instru_name != "") & (first_instru_telephone != "")):
#                try:
#                    zhidao1 = models.Instructor.objects.get(name = first_instru_name, 
#                                                   telephone = first_instru_telephone)
#                    zhidao1.team.add(team)
#                    team.first_instru_telephone = first_instru_telephone
#                    team.save()
#                except:
#                    zhidao1_error = "没有该指导老师信息"
#                    return render(request, 'info-team.html', locals())
            
            #=======save=========
            
#            if ((second_instru_name != "") & (second_instru_telephone != "")):
#                try:
#                    zhidao2 = models.Instructor.objects.get(name = second_instru_name, 
#                                                   telephone = second_instru_telephone)
#                    zhidao2.team.add(team)
#                except:
#                    zhidao2_error = "没有该指导老师信息"
#                    return render(request, 'info-team.html', locals())
            
                

            #指导老师信息不完整创建处理           
            if (((first_instru_name == "") & (first_instru_telephone != "")) | ((first_instru_name != "") & (first_instru_telephone == ""))):
                zhidao1_error = "第一指导老师信息不完整"
                return render(request, 'info-team.html', locals())

            if (((second_instru_name == "") & (second_instru_telephone != "")) | ((second_instru_name != "") & (second_instru_telephone == ""))):
                zhidao2_error = "第二指导老师信息不完整"
                return render(request, 'info-team.html', locals())

            #指导老师已存在该团队中，再次修改处理
            if ((ftele != "") & (first_instru_telephone != "")):
                if (ftele != first_instru_telephone):
                    print("清扫--01")
                    team.instru.clear()
            if ((stele != "") & (second_instru_telephone != "")):
                if (stele != second_instru_telephone):
                    print("清扫--02")
                    team.instru.clear()
            
                #指导老师信息完整，判断是否存入数据库
            if ((first_instru_name != "") & (first_instru_telephone != "")):
                
                try:
                    zd = models.Instructor.objects.get(telephone = first_instru_telephone)
                    print("已有该第一指导老师")
                    zd.name = first_instru_name
                    zd.team.add(team)
                    zd.save()
                    team.first_instru_telephone = first_instru_telephone
                    team.save()

                except:
                    zhidao1 = models.Instructor.objects.create(name = first_instru_name, 
                                                       telephone = first_instru_telephone,
                                                       school = school)
    
                    zhidao1.team.add(team)
                    team.first_instru_telephone = first_instru_telephone
                    team.save()

            
            
            if ((second_instru_name != "") & (second_instru_telephone != "")):
                
                try:
                    zd = models.Instructor.objects.get(telephone = second_instru_telephone)
                    print("已有该第二指导老师")
                    zd.name = second_instru_name
                    zd.team.add(team)
                    zd.save()
                    team.save()
                except:
                    zhidao2 = models.Instructor.objects.create(name = second_instru_name, 
                                                           telephone = second_instru_telephone,
                                                           school = school)
                    zhidao2.team.add(team)
                    team.save()
            
            return render(request, 'info-team.html', locals())
        else:
            file_error = forms.get_errors(teamInfoForm)
            print(teamInfoForm.errors.get_json_data())
            return render(request, 'info-team.html', locals())
            

def del_member2(request, member_tele):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team    
    try:
        memb = models.Member.objects.get(telephone = member_tele)
        memb.delete()
        team.tele_member2 = "00000"
        team.save()
        return redirect(reverse("team:teaminfo"))
    except:
        return HttpResponse("没有找到该队员信息,删除失败")

def del_member3(request, member_tele):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team    
    try:
        memb = models.Member.objects.get(telephone = member_tele)
        memb.delete()
        team.tele_member3 = "00000"
        team.save()
        return redirect(reverse("team:teaminfo"))
    except:
        return HttpResponse("没有找到该队员信息,删除失败")


def team_save_submit(request):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team
    if request.method == "GET":
        return render(request, "team-save-submit.html", locals())
    elif request.method == "POST":
        choose = request.POST.get("choose")
        print(choose)
        if choose == "1":
            team.status = "待审核"
            team.save()
            return redirect(reverse("team:savesubmit"))
        elif choose == "0":
            return redirect(reverse("team:teaminfo"))

def team_part_info_team_over(request):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team
    instructors = team.instru.all()
    print(instructors)
    if instructors:
        for i in instructors:
            if i.telephone == team.first_instru_telephone:
                first_instruc = i
            else:
                second_instruc = i
    
    if team.tele_member2 != "00000":
        print(team.tele_member2)
        member2 = models.Member.objects.get(telephone = team.tele_member2)
    else:
        member2 = ""
        
    if team.tele_member3 != "00000":
        member3 = models.Member.objects.get(telephone = team.tele_member3)
    else:
        member3 = ""
    
    if request.method == "GET":
        return render(request, "submit-team-info.html", locals())
    elif request.method == "POST":
        return HttpResponse("<h1>没有POST方法!</h1>")


def upload_word_pdf(request):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team
    if request.method == "GET":
        return render(request, "upload-work-word-pdf-cc.html", locals())
    elif request.method == "POST":
        workForm = forms.WorkForm(request.POST, request.FILES)
        if workForm.is_valid():
            print("我进入clean了")
            work_commit = request.FILES.get("paper_commit", None)
            work_sign_up = request.FILES.get("paper_sign_up", None)
            work_game_data = request.FILES.get("paper_game_data", None)
            work_word = request.FILES.get("paper_word", None)
            work_pdf = request.FILES.get("paper_pdf", None)
            work_cc = request.FILES.get("paper_cc", None)
            
            try:
                work = models.Work.objects.get(work_id = team)
                print("get成功")
            except:
                raise Http404
            if ((work_word is None) & (work_pdf is None)) & (work.paper_word is None) & (work.paper_pdf is None):
                print(work.paper_word)
#                print(work_word)
                status = "未上传"
            else:
                status = "已上传"
                my_massage = []
                if work_word is not None:
                    if work_word.size > 10485760:
                        word_size_error = "上传文件过大"
                        return render(request, "upload-work-word-pdf-cc.html", locals())
                    
                    print(work_word.name)
                    print(work_word.size)
                    print(team.work_id+".doc")
                    
                    if ((work_word.name != team.work_id+".doc") & (work_word.name != team.work_id+".docx")):
                        word_name_error = "文件命名不规范"
                        return render(request, "upload-work-word-pdf-cc.html", locals())
                    my_massage.append("作品word版上传成功")
                    work.paper_word = work_word
                    
                if work_pdf is not None:
                    if work_pdf.size > 10485760:
                        pdf_size_error = "上传文件过大"
                        return render(request, "upload-work-word-pdf-cc.html", locals())
                    
                    print(work_pdf)
                    
                    if (work_pdf.name != team.work_id+".pdf"):
                        pdf_name_error = "文件命名不规范"
                        return render(request, "upload-work-word-pdf-cc.html", locals())
                    
                    my_massage.append("作品pdf版上传成功")
                    work.paper_pdf = work_pdf
                    
                if work_cc is not None:
                    if work_pdf.size > 10485760:
                        cc_size_error = "上传文件过大"
                        return render(request, "upload-work-word-pdf-cc.html", locals())

                    if (work_cc.name != team.work_id+"_cc.pdf"):
                        cc_name_error = "文件命名不规范"
                        return render(request, "upload-work-word-pdf-cc.html", locals())

                    my_massage.append("查重文件上传成功")
                    work.paper_cc = work_cc
            
                if work_commit is not None:
                    if work_commit.size > 10485760:
                        commit_size_error = "上传文件过大"
                        return render(request, "upload-work-word-pdf-cc.html", locals())

                    if (work_commit.name != team.work_id+"_commit.pdf"):
                        commit_name_error = "文件命名不规范"
                        return render(request, "upload-work-word-pdf-cc.html", locals())

                    my_massage.append("承诺书上传成功")
                    work.paper_commit = work_commit

                if work_sign_up is not None:
                    if work_sign_up.size > 10485760:
                        sign_up_size_error = "上传文件过大"
                        return render(request, "upload-work-word-pdf-cc.html", locals())

                    if ((work_sign_up.name != team.work_id+"_sign_up.doc") & (work_sign_up.name != team.work_id+"_sign_up.docx")):
                        sign_up_name_error = "文件命名不规范"
                        return render(request, "upload-work-word-pdf-cc.html", locals())
                    my_massage.append("报名表上传成功")
                    work.paper_sign_up = work_sign_up


                if work_game_data is not None:
                    if work_game_data.size > 10485760:
                        game_data_size_error = "上传文件过大"
                        return render(request, "upload-work-word-pdf-cc.html", locals())

                    if (work_game_data.name != team.work_id+"_game_data.zip") & (work_game_data.name != team.work_id+"_game_data.rar"):
                        game_data_name_error = "文件命名不规范"
                        return render(request, "upload-work-word-pdf-cc.html", locals())

                    my_massage.append("原始数据上传成功")
                    work.paper_game_data = work_game_data

            
            work.status = status
            work.save()
            html = "<h1>作品word/pdf版{}成功</h1>".format(status)
            for m in my_massage:
                html += "<br> 新增信息: " + m
            return HttpResponse(html)
        else:
            file_error = forms.get_errors(workForm)
            return render(request, "upload-work-word-pdf-cc.html", locals())


def team_part_work_upload(request):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team
    if request.method == "GET":
        return render(request, 'team-work-upload.html', locals())
    elif request.method == "POST":
        return HttpResponse("此界面无POST方法.")
        
def reg_member(request):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    team = captain.team
    
    temp_list = [team.tele_member2, team.tele_member3]
    member_list = [item for item in temp_list if item != "00000"]
    print(member_list)
    member_len = len(member_list)
    
    if request.method == 'GET':
        if (member_len == 2):
            return HttpResponse("<h2>团队已满3人,无法添加队员</h2> <div>若要更换队员请删除现有队员！</div>")
        else:
            return render(request, 'reg-member-info.html', locals())
    elif request.method == 'POST':
        memberForm = forms.MemberForm(request.POST, request.FILES)
        if memberForm.is_valid():
            member_name = memberForm.cleaned_data.get('member_name')
            grade = memberForm.cleaned_data.get('grade')
            telephone = memberForm.cleaned_data.get('telephone')
            
            id_number = request.POST.get("id_number", "")
            student_number = request.POST.get("student_number", "")
            major = request.POST.get("major", "")
            class_in_school = request.POST.get("class_in_school", "")
            
            member = models.Member.objects.create(member_name = member_name,
                                                  grade = grade,
                                                  telephone = telephone,
                                                  id_number = id_number,
                                                  student_number = student_number,
                                                  major = major,
                                                  class_in_school = class_in_school)
            if (member_len == 0):
                print("2个队员都没填写,现在我要增加队员2了")
                team.tele_member2 = telephone
                team.save()
            elif (member_len == 1):
                print("1个队员没填写,现在我要增加队员3了")
                team.tele_member3 = telephone
                team.save()
            return render(request, "team-info-team-success.html", locals())
        else:
            file_error = forms.get_errors(memberForm)
            print(memberForm.errors.get_json_data())
            return render(request, 'reg-member-info.html', locals())


def reg_captain(request):
    session_team = request.session.get('userinfo', '')
    telephone = session_team['telephone']
    captain = models.Member.objects.get(telephone = telephone)
    if request.method == 'GET':
        return render(request, 'reg-captain-info.html', locals())
    elif request.method == 'POST':
        captainForm = forms.CaptainForm(request.POST, request.FILES)
        if captainForm.is_valid():
#            member_name = captainForm.cleaned_data.get('member_name')
            grade = captainForm.cleaned_data.get('grade')
            
#            captain.member_name = member_name
            captain.grade = grade
            
            id_number = request.POST.get("id_number", "")
            student_number = request.POST.get("student_number", "")
            major = request.POST.get("major", "")
            class_in_school = request.POST.get("class_in_school", "")
            
            captain.id_number = id_number
            captain.student_number = student_number
            captain.major = major
            captain.class_in_school = class_in_school
            captain.is_captain = "是"
            captain.save()
            
            return render(request, "team-info-team-success.html", locals())
        else:
            file_error = forms.get_errors(captainForm)
            print(captainForm.errors.get_json_data())
            return render(request, 'reg-captain-info.html', locals())
    






#=========测试===========

def add_default_instruc(request):
    school = models.College.objects.get(school = "安徽财经大学")
    user = models.Instructor.objects.create(name = "无此人二",
                                            telephone = "14404404404",
                                            password = "19970928",
                                            school = school)
    return HttpResponse("<h1>添加成功!</h1>")

def temp_index_team(request):
    
    return HttpResponse("<h1>团队临时主页</h1>")

def team_test(request):
    school = models.College.objects.get(school = "安徽工业大学")
    print(school)
    print(school.school)
    user = models.Team.objects.create(school = school,
                                       captain = "小王",
                                       telephone = "15495298980",
                                       password = "19970928")
    return HttpResponse("<h1>Success!</h1>")