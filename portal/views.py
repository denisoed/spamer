# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib import auth
from .forms import PortalForm
from .list_portals import list_portals
from .tasks import get_login_page
from .models import Portal


def catch_portal_form(request):
    if request.method == 'POST':
        portal_form = PortalForm(request.POST or None)
        if portal_form.is_valid():
            selected_portal = portal_form.save(commit=False)
            login = portal_form.cleaned_data['login']
            password = portal_form.cleaned_data['password']
            return selected_portal, login, password

        else:
            messages.error(request, "Форма не валидна")
            return redirect('/main/')
    else:
        return HttpResponseRedirect('/main/')


def create_portal(request):
    verificated_data = catch_portal_form(request)
    obj_portal = find_selected_portal(request)
    print(obj_portal)
    selected_portal = verificated_data[0]
    login = verificated_data[1]
    password = verificated_data[2]
    if Portal.objects.filter(name=selected_portal.name):
        messages.error(request, "Портал уже существует в вашем списке!")
    else:
        auth_portal_complate = get_login_page(request, obj_portal,
                                              login, password)
        if auth_portal_complate is True:
            user = auth.get_user(request).username
            selected_portal.user = user
            selected_portal.save()
            return redirect('/main/')
        else:
            messages.error(request,
                           "Не получилось аутентифицироваться на портале")


def find_selected_portal(request):
    for i in range(len(list_portals)):
        if list_portals[i]['name'] == request.POST.get('portals'):
            portal = list_portals[i]
            return portal


def delete_portal(request, id_portal):
    portal = Portal.objects.filter(pk=id_portal)
    portal.delete()
    return redirect('/main/')
