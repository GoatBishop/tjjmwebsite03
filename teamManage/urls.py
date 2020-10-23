# -*- coding: utf-8 -*-

from django.urls import path,include,re_path
from . import views

app_name = 'team'

urlpatterns = [
    path('login/', views.mylogin, name = "tlogin"),
    path('logout/', views.mylogout, name = "tlogout"),
    path('temp_index_team/',  views.temp_index_team, name = "tempteammain"),
    path('register/', views.myregister, name = "treg"),
    path('repsw/', views.repsw, name = "tresetpsw"),
    path('testreg/', views.team_test),
    path('team_index/', views.team_index, name = "teammain"),
    path('team_info/', views.team_part_info_team, name = "teaminfo"),
    path('add_default_instruc/', views.add_default_instruc),
    path('work_upload/', views.team_part_work_upload, name = "workupload"),
    path('reg_captain/', views.reg_captain, name = "regcaptain"),
    path('reg_team_member/', views.reg_member, name = "regmember"),
    re_path(r'^del_memb2/(\w+)/$', views.del_member2),
    re_path(r'^del_memb3/(\w+)/$', views.del_member3),
    path('save_submit/', views.team_save_submit),
    path('team_part_info_team_over/', views.team_part_info_team_over, name = "savesubmit"),
    path('upload_word_pdf/', views.upload_word_pdf, name = "uploadwordpdf"),
]