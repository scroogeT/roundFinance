# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from .models import *
from django.shortcuts import render

# Create your views here.

def index(request):
   return render(request,'dash/index.html')

def profile(request):
    currUser = request.user

    #drivr = driver.objects.get(user=request.user)
    pendingState = memberState.objects.get(status="pending")
    #myProf = members.objects.get_or_create(user = currUser,defaults={'status':pendingState,'maskedName':currUser.username})
    myProf = members.objects.get(user=currUser)
    print(myProf)
    return render(request, 'dash/profile.html',{"myProf":myProf})

def account_history(request):       #transactions where the logged in user was involved
    currUser = request.user
    myTrans = transactions.objects.filter(Q(borrower=currUser.username)|Q(lender=currUser.username))
    print (myTrans)
    return render(request, 'dash/account_history.html',{'myTrans':myTrans})