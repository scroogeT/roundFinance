# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View, CreateView, UpdateView, DeleteView

from .forms import transactionsForm

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    currUser = request.user

    myCredits = transactions.objects.filter(lender__exact=currUser.username)
    myDebt = transactions.objects.get(Q(borrower__exact=currUser.username)&Q(status__state='pending'))

    try:
        myArrears = paybackInstallments.objects.get(transaction=myDebt)
    except:
        paybackInstallments.objects.create(transaction=myDebt, defaults={"transaction": myDebt})
        myArrears = paybackInstallments.objects.get(transaction=myDebt)

    return render(request,'dash/index.html',{'myCredits':myCredits,'myDebt':myDebt,"myArrears":myArrears})

#TODO: login required mixin
class profileView(View):
    def get(self, request):
        currUser = request.user

        # drivr = driver.objects.get(user=request.user)
        pendingState = memberState.objects.get(status="pending")
        # myProf = members.objects.get_or_create(user = currUser,defaults={'status':pendingState,'maskedName':currUser.username})
        myProf = members.objects.get(user=currUser)
        print(myProf)
        return render(request, 'dash/profile.html', {"myProf": myProf})

@login_required(login_url='/login/')
def account_history(request):       #transactions where the logged in user was involved
    currUser = request.user
    myTrans = transactions.objects.filter(Q(borrower=currUser.username)|Q(lender=currUser.username))
    print (myTrans)
    return render(request, 'dash/account_history.html',{'myTrans':myTrans})

@login_required(login_url='/login/')
def borrowerList(request):
    borrowers = transactions.objects.filter(status__state='waiting')
    return render(request, 'dash/borrowerList.html',{"borrowers":borrowers})

@login_required(login_url='/login/')
def borrowerProfile(request):
    return  render(request, 'dash/borrowerProfile.html')
#TODO: change this to use profileDetail

class debtPayment(UpdateView):
    model = paybackInstallments
    fields = ('installment1','description1','proofOfPayment1',
              'installment2', 'description2', 'proofOfPayment2',
              'installment3', 'description3', 'proofOfPayment3')
    template_name = 'dash/paybackDebt.html'
    success_url = reverse_lazy('dashboard')
    pk_url_kwarg = 'trans_pk'
    #pk_url_kwarg = paybackInstallments.objects.get(transaction_id=trans_pk)

def creditDetail(request, pk):

    myDebt = transactions.objects.get(pk=pk)
    try:
        myArrears = paybackInstallments.objects.get(transaction=myDebt)
    except:
        paybackInstallments.objects.get_or_create(transaction=myDebt, defaults={"transaction": myDebt})
        myArrears = paybackInstallments.objects.get(transaction=myDebt)

    return render(request,'dash/creditDetail.html',{"myDebt":myDebt,"myArrears":myArrears})

class receivePayment(UpdateView):
    model = paybackInstallments
    fields = ('received1','received2','received3')
    template_name = 'dash/paybackDebt.html'
    success_url = reverse_lazy('dashboard')
    pk_url_kwarg = 'trans_pk'


#TODO: after creating an account, a repayment account must be provisioned
class newDebt(CreateView):
    model = transactions
    form_class = transactionsForm
    success_url = reverse_lazy('dashboard')
    template_name = 'dash/borrowFunds.html'

    def form_valid(self, form):
        # check if theere are no pending/ queued / waiting(unfullfilled) debts by the user
        currUsername = self.request.user.username
        # queuedTrans = transactionState.objects
        pendingTrans = transactions.objects.filter(Q(borrower__exact=currUsername) & (
        Q(status__state__exact='pending') | Q(status__state__exact='waiting') | Q(status__state__exact='queued')))
        if pendingTrans:
            print("you cannot borrow more funds you have pending Trans!!!")
            return redirect('dashboard')
        else:
            newTransaction = form.save(commit=False)
            # manually handle the other hidden fields required to initiate a transaction
            newTransaction.borrower = self.request.user.username
            newTransaction.status = transactionState.objects.get(state="queued")
            newTransaction.save()
            print("request logged..")
            return redirect('dashboard')

class updateProfile(UpdateView):
    model = members
    success_url = reverse_lazy('profile')
    fields = ("phone","profPic","idNum","Address","proofOfResidence","proofOfID","maskedName")
    template_name = 'dash/profileUpdate_form.html'
    pk_url_kwarg = 'member_pk'

    def form_valid(self, form):
        post = form.save(commit=False)
        print("chaita")
        post.save()
        return redirect('profile')