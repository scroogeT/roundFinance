# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request,'public/home.html')

def about(request):
    return render(request,'public/about.html')

def contact(request):
    return render(request, 'public/contact.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})