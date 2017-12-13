# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register_user(request):
    form = UserCreationForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(
                                    username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            auth.login(request, new_user)
            return redirect('/account/login/')
        else:
            messages.error(request, "Ошибка сервера")
    else:
        return render(request, 'register.html', context)


def authorization_user(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(username=login, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/main/')
        else:
            return redirect('/account/login/')
    else:
        return render(request, 'login.html')


def logout_user(request):
    auth.logout(request)
    return redirect('/main/')
