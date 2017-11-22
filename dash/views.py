# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from .models import *
from django.shortcuts import render,redirect

from .forms import transactionsForm

# Create your views here.

def index(request):
    currUser = request.user

    myCredits = transactions.objects.filter(lender__exact=currUser.username)
    myDebts = transactions.objects.filter(borrower__exact=currUser.username)

    print(myDebts,myCredits)

    return render(request,'dash/index.html',{'myCredits':myCredits,'myDebts':myDebts})

def profile(request):
    currUser = request.user

    #drivr = driver.objects.get(user=request.user)
    pendingState = memberState.objects.get(status="pending")
    #myProf = members.objects.get_or_create(user = currUser,defaults={'status':pendingState,'maskedName':currUser.username})
    myProf = members.objects.get_or_create(user=currUser,defaults={'user':request.user,'status':pendingState,'maskedName':currUser.username})
    print(myProf)
    return render(request, 'dash/profile.html',{"myProf":myProf})

def account_history(request):       #transactions where the logged in user was involved
    currUser = request.user
    myTrans = transactions.objects.filter(Q(borrower=currUser.username)|Q(lender=currUser.username))
    print (myTrans)
    return render(request, 'dash/account_history.html',{'myTrans':myTrans})

def borrowerList(request):
    borrowers = transactions.objects.filter(status__state='waiting')
    return render(request, 'dash/borrowerList.html',{"borrowers":borrowers})

def borrowerProfile(request):
    return  render(request, 'dash/borrowerProfile.html')

def borrowFunds(request):
    if request.method == 'POST':
        # check if theere are no pending/ queued / waiting(unfullfilled) debts by the user
        currUsername = request.user.username
        #queuedTrans = transactionState.objects
        pendingTrans = transactions.objects.filter(Q(borrower__exact=currUsername) & (Q(status__state__exact='pending')|Q(status__state__exact='waiting')|Q(status__state__exact='queued')))
        if pendingTrans:
            print("you cannot borrow more funds you have pending Trans!!!")
            return redirect('dashboard')
        else:
            form = transactionsForm(request.POST)
            if form.is_valid():
                newTransaction = form.save(commit=False)
                # manually handle the other hidden fields required to initiate a transaction
                newTransaction.borrower = request.user.username
                newTransaction.status = transactionState.objects.get(state="queued")
                newTransaction.save()
                print("request logged..")
                return redirect('dashboard')
    else:
        form = transactionsForm()

    return render(request,'dash/borrowFunds.html',{"form":form})