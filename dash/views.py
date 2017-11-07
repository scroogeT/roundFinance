# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
   return render(request,'dash/index.html')

def profile(request):
    return render(request, 'dash/profile.html')

def account_history(request):
    return render(request, 'dash/account_history.html')