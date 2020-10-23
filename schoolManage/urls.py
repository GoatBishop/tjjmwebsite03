# -*- coding: utf-8 -*-

from django.urls import path,re_path
from .  import views
app_name = 'school'

urlpatterns = [
    path('login/', views.mylogin, name = "slogin"),
    path('register/', views.myregister, name = "sreg"),
    path('repsw/', views.repsw, name = "resetPassword"),
    path('college_index/', views.college_index, name = "collegemain"),
    path('chpsw/', views.chpsw, name = "changepassword"),
#    path('noauditteam/', views.noauditteam, name = "noAuditTeam"),
    path('testpage/', views.testPage, name = "test"),
    path('part_school_teacher/', views.part_school_teacher, name = "schoolteacher"),
    path('part_game_team/', views.part_game_team, name = "game_team"),
    path('part_game_team_all/', views.part_game_team_all, name = "game_team_all"),
    path('part_game_paper/', views.part_game_paper, name = "gamepaper"),
    path('part_game_paper_all/', views.part_game_paper_all),
    re_path(r'instruc_del/(\w+)/', views.instruc_del),
    path('testupload/', views.testupload),
    path('logout/', views.mylogout, name = "slogout"),
    path('test_school_list/', views.test_school_list),
    re_path(r'team_pass/(\w+)/', views.team_pass),
    re_path(r'team_no_pass/(\w+)/', views.team_no_pass),
    re_path(r'excel_download/(\w+)/', views.excel_download),
    re_path(r'pdf_download/(\w+)/', views.pdf_download),
    re_path(r'word_download/(\w+)/', views.word_download),
    re_path(r'submit/(\w+)/', views.my_submit),
    re_path(r'tuihui/(\w+)/', views.my_tuihui),
]