from django.contrib import admin

# Register your models here.
from . import models

#为了让 admin 界面管理某个数据模型,需要先注册该数据模型到admin

class College_Manager(admin.ModelAdmin):
    list_display = ["school", "contacts", "contacts_telephone", 
                    "admin_verification", "number_team", "add_time"]
    search_fields = ["school", "contacts_telephone", "audit_status"]
    
    list_editable = ["number_team", "admin_verification"]
    list_filter = ["audit_status"]

admin.site.register(models.College, College_Manager)

class Instructor_Manager(admin.ModelAdmin):
    list_display = ["name", "telephone", "id_number", 
                    "school", "add_time"]
    search_fields = ["name", "telephone"]
    list_filter = ["school"]

admin.site.register(models.Instructor, Instructor_Manager)

class Team_Manager(admin.ModelAdmin):
    list_display = ["work_id", "group", "telephone", "work_group", 
                    "school", "status", "add_time"]
    search_fields = ["school", "telephone", "group", "status"]
    list_filter = ["group", "status"]

admin.site.register(models.Team, Team_Manager)

class Work_Manager(admin.ModelAdmin):
    list_display = ["work_id", "paper_word", "paper_pdf", 
                    "paper_cc", "status", "add_time"]
    list_filter = ["status"]

admin.site.register(models.Work, Work_Manager)

class Judge_Manager(admin.ModelAdmin):
    list_display = ["judge_username", "judge_name", "password", 
                    "judge_type", "add_time"]
    list_editable = ["judge_name", "password", "judge_type"]
    list_filter = ["judge_type"]

admin.site.register(models.Judge, Judge_Manager)

class Score_Manager(admin.ModelAdmin):
    list_display = ["judge", "judge_score", 
                    "judge_detail", "judge_is_review"]
    list_editable = ["judge_score"]
    list_filter = ["judge"]

admin.site.register(models.Score, Score_Manager)
