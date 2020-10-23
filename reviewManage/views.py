from django.shortcuts import render
from backManage import models
from backManage import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,reverse
from django.views.generic.base import View

def mylogin(request):
    if request.method == 'GET':
        print("reviewManage: 我是mylogin的GET")
        judge_username = request.COOKIES.get('judge_username', '')
        return render(request, 'login-review.html', locals())
    elif request.method == 'POST':
        # 获取表单的数据
        print("reviewManage: 我是mylogin的POST")
        judge_username = request.POST.get('judge_username', '')
        password = request.POST.get('password', '')
        print(judge_username, "--", password)
#        # 验证用户名，密码是否正确
        try:
            print("我进入mylogin的try里来了")
            user = models.Judge.objects.get(judge_username = judge_username,
                                           password = password)
            print(user)
            print("我存在数据库中")
            # 在当前连接的Session中记录当前用户的信息
            request.session['userinfo'] = {
                "judge_username": user.judge_username,
            }
        except:
            #登录失败
            print("我登录失败了")
            return render(request, 'login-review.html', locals())
        # 处理COOKIES
        print("我要跳转到login-review.html")
        resp = redirect(reverse('review:rmain'))
        resp.set_cookie('judge_username', judge_username, 5*24*60*60)
        print("我已经设置了cookie")
        return resp

def review_main(request):
    session_review = request.session.get('userinfo', '')
    if session_review:
        print("session_review", session_review)
        judge_username = session_review['judge_username']
        user = models.Judge.objects.get(judge_username = judge_username)
        judge_name = user.judge_name
        return render(request, "index-review.html", locals())
    else:
        print("我没有session")
        return redirect(reverse('review:rlogin'))

def no_review_work(request):
    session_review = request.session.get('userinfo', '')
    judge_username = session_review['judge_username']
    judge = models.Judge.objects.get(judge_username = judge_username)
    scores = models.Score.objects.filter(judge = judge, judge_is_review = "否")
#    scores = models.Score.objects.filter(judge = judge)
    
    print(scores)
    if scores:
        works = [s.work for s in scores]
        teams = [w.work_id for w in works]
        
        for s in scores:
            print(s.judge_is_review)
    else:
        works = []
    if request.method == "GET":
        return render(request, 'work-no-review.html', locals())
    elif request.method == "POST":
        return HttpResponse("此界面无POST方法.")

def judge_score(request, work_id):
    session_review = request.session.get('userinfo', '')
    judge_username = session_review['judge_username']
    judge = models.Judge.objects.get(judge_username = judge_username)
    team = models.Team.objects.get(work_id = work_id)
    work =  models.Work.objects.get(work_id = team)
    score = models.Score.objects.get(work = work, judge = judge)
    print(score)
    print(work_id)
    is_submit_judge = score.judge_is_review
    if request.method == "GET":
        return render(request, "judge-score.html", locals())
    elif request.method == "POST":
        workScoreForm = forms.WorkScoreForm(request.POST, request.FILES)
        if workScoreForm.is_valid():
            score_ponit = request.POST.get("score_ponit", "")
            my_score = request.POST.get("score", "")
            score.judge_score = int(my_score)
            score.judge_detail = score_ponit
            score.judge_is_review = "是"
            is_submit_judge = score.judge_is_review
            
            score.save()
            judge_detail = score_ponit
            judge_score = score
            return redirect(reverse("review:rnoreviewwork"))
        else:
            file_error = forms.get_errors(workScoreForm)
            print(workScoreForm.errors.get_json_data())
            return render(request, 'judge-score.html', locals())           
        
def score_temp(request, work_id):
    session_review = request.session.get('userinfo', '')
    judge_username = session_review['judge_username']
    judge = models.Judge.objects.get(judge_username = judge_username)
    team = models.Team.objects.get(work_id = work_id)
    work =  models.Work.objects.get(work_id = team)
    score = models.Score.objects.get(work = work, judge = judge)
    
    is_submit_judge = "否"
    
    if request.method == "POST":
        workScoreForm = forms.WorkScoreForm(request.POST, request.FILES)
        if workScoreForm.is_valid():
            score_ponit = request.POST.get("score_ponit", "")
            score_num = request.POST.get("score", "")
            score.judge_score = int(score_num)
            score.judge_detail = score_ponit
            score.save()
            return redirect(reverse("review:rnoreviewwork"))
        else:
            file_error = forms.get_errors(workScoreForm)
            print(workScoreForm.errors.get_json_data())
            return render(request, 'judge-score.html', locals())           

def already_review_work(request):
    session_review = request.session.get('userinfo', '')
    judge_username = session_review['judge_username']
    judge = models.Judge.objects.get(judge_username = judge_username)
    scores = models.Score.objects.filter(judge = judge, judge_is_review = "是")
    works = [s.work for s in scores]
    teams = [w.work_id for w in works]
    if request.method == "GET":
        return render(request, 'work-already-review.html', locals())
    elif request.method == "POST":
        return HttpResponse("此界面无POST方法.")


def judge_already_score(request, work_id):
    session_review = request.session.get('userinfo', '')
    judge_username = session_review['judge_username']
    judge = models.Judge.objects.get(judge_username = judge_username)
    team = models.Team.objects.get(work_id = work_id)
    work =  models.Work.objects.get(work_id = team)
    score = models.Score.objects.get(work = work, judge = judge)
    score_ponit = score.judge_detail
    score = score.judge_score
    work_score = models.Score.objects.filter(work = work)
    score_list = [s.judge_score for s in work_score]
    score_list_limit = [int(sl) for sl in score_list if sl != "0"]
    ave_score = round(sum(score_list_limit)/len(score_list_limit), 2)
    return render(request, 'judge-score-details.html', locals())

def mylogout(request):
    if 'userinfo' in request.session:
        del request.session['userinfo']
    return redirect(reverse('review:rlogin'))
    