# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime,timedelta
from django.utils.timezone import get_current_timezone, is_aware
# Create your models here.

class memberState(models.Model):
    status = models.CharField(max_length=25)
    description = models.TextField(max_length=50)
    def __str__(self):
        return str(self.status)

class members(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(blank=True, max_length=15)
    profPic = models.ImageField(blank=True)
    idNum = models.CharField(blank=True,max_length=20)
    Address = models.TextField(blank=True,max_length=200)
    proofOfResidence = models.ImageField(blank=True)
    proofOfID = models.ImageField(blank=True)
    canBorrow = models.BooleanField(default=False)
    borrowingCeiling = models.FloatField(blank=True, default=0)
    maskedName = models.CharField(blank=True, max_length=30)
    status = models.ForeignKey(memberState, blank=True)

    def __str__(self):
        return str(str(self.user.username)+':'+str(self.user.first_name)+' '+str(self.user.last_name))

#timeNow = datetime.now(tz='Africa/Harare')

class transactionState(models.Model):
    state = models.CharField(max_length=20)
    description = models.TextField(max_length=50)

    def __str__(self):
        return str(self.state)

class transactions(models.Model):
    borrower = models.CharField(blank=False,max_length=30)
    amount = models.FloatField(blank=False)
    amountPaid = models.FloatField(blank=True, default=0)
    datePosted = models.DateTimeField(blank=False, default=datetime.now())
    status = models.ForeignKey(transactionState)
    dueDate = models.DateTimeField(blank=True, default=(datetime.now() + timedelta(days=30)))
    descriptionOfUse = models.TextField(blank=True, max_length=200)
    lender = models.CharField(max_length=30, blank=True)
    lendingDate = models.DateTimeField(blank=True,default=(datetime.now() + timedelta(days=30)))

    def __str__(self):
        return str(self.borrower)+' from '+str(self.lender)+' amount '+ str(self.amount)

"""
Members are users with the following attibutes:
    phone
    address
    profile picture
    bank name
    bank account number
    proof of residence
    guarantor
    Member_status(active,suspended,onHold)
    MemberType(borrower, lender, either)
    isEligibleToBorrow(Boolean)
    
Borrowings:
    memberID
    date borrowed
    amount
    date_of_repayment
    amnt_repaid
    
"""
