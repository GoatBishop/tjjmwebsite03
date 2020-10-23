# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

def mainIndex(request):
    return render(request, "main.html", locals())

def welcome(request):
    return render(request, "welcome.html")