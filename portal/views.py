# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib import auth
from .forms import PortalForm
from .list_portals import list_portals
from .models import Portal


def create_portal(request):
    if request.method == 'POST':
        portal_form = PortalForm(request.POST or None)
        if portal_form.is_valid():
            selected_portal = portal_form.save(commit=False)
            login = portal_form.cleaned_data['login']
            password = portal_form.cleaned_data['password']
            if Portal.objects.filter(name=selected_portal.name):
                messages.error(
                    request, "Портал уже существует в вашем списке!")
            else:
                create_new_portal(request, login,
                                  password, selected_portal)
        else:
            messages.error(request, "Форма не валидна")
        return redirect('/main/')
    else:
        return HttpResponseRedirect('/main/')


def create_new_portal(request, login, password,
                      selected_portal):
    user = auth.get_user(request)
    selected_portal.user = user
    selected_portal.login = login
    selected_portal.password = password
    selected_portal.save()
    return redirect('/main/')


def find_selected_portal(portal_name):
    for i in range(len(list_portals)):
        if list_portals[i]['name'] == portal_name:
            portal = list_portals[i]
            return portal


def delete_portal(request, id_portal):
    portal = Portal.objects.filter(pk=id_portal)
    portal.delete()
    return redirect('/main/')
