# -*- coding: utf-8 -*-

from django.urls import path,include, re_path
from . import views
app_name = 'review'

urlpatterns = [
    path('login/', views.mylogin, name = "rlogin"),
    path('logout/', views.mylogout, name = "rlogout"),
    path('review_main/', views.review_main, name = "rmain"),
    path('no_review_work/', views.no_review_work, name = "rnoreviewwork"),
    path('already_review_work/', views.already_review_work, name = "ralreadyreviewwork"),
    re_path(r'judge_score/(\w+)/', views.judge_score, name = "judgescore"),
    re_path(r'score_temp/(\w+)/', views.score_temp),
    re_path(r'judge_already_score/(\w+)/', views.judge_already_score, name = "judgealreadyscore"),
]