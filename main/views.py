# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import auth
from portal.forms import PortalForm
from portal.models import Portal
from portal.tasks import send_spam


def catch_data(request):
    portal_form = PortalForm()
    portals_user = Portal.objects.filter(user=auth.get_user(request).username)
    context = {
        'portal_form': portal_form,
        'portals_user': portals_user,
        'user': auth.get_user(request).username
    }
    if request.method == 'POST':
        portal_form = PortalForm(request.POST or None)

        portal_sel = request.POST.getlist('selected_portal')
        if request.POST.get('title') == '' \
                and request.POST.get('url') == '':
            context = {
                'empty': 'Это поле обязательное!'}
        else:
            input_data = {
                'login': portals_user[0].login,
                'password': portals_user[0].password,
                'title': request.POST.get('title'),
                'url': request.POST.get('url'),
                'description': request.POST.get('description')
            }
            context = {
                'portal_form': portal_form
            }
            send_spam.delay(input_data, portal_sel)
        return redirect('/main/')
    return render(request, 'index.html', context)
