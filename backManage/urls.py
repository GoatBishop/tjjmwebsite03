# -*- coding: utf-8 -*-


from django.urls import path,include,re_path
from . import views


app_name = 'back'

urlpatterns = [
    path('login/', views.mylogin, name = 'blogin'),
    path('logout/', views.mylogout, name = 'blogout'),
    path('back_main/', views.back_main, name = 'bmain'),
    path('work_list/', views.work_list, name = 'worklist'),
    path('judge_list/', views.judge_list, name = 'judgelist'),
    path("random_one/", views.random_one),
    path("random_many/", views.random_many),
    path('wait_round2_list/', views.wait_round2_list, name = 'waitround2list'),
    path('rounding2_list/', views.rounding2_list, name = 'rounding2list'),
    path('rounded2_list/', views.rounded2_list, name = 'rounded2list'),
    path('team_situation/', views.team_situation, name = 'teamsituation'),
    re_path(r'tuihui/(\w+)/', views.tuihui, name = "tuihui"),
    re_path(r'excel_download/(\w+)/', views.excel_download, name = "tuihui"),
    re_path(r'file_download/(\w+)/', views.file_download),
    path('assign_judges/', views.assign_judges)
]
