from django.shortcuts import render, redirect
from .forms import PortalForm
from .list_portals import list_portals
from main.handler import auth_portal
from .models import Portal
from django.contrib import messages
from django.contrib import auth


def create_portal(request):
    if request.method == 'POST':
        log_pass = {
            'login': request.POST.get('login'),
            'password': request.POST.get('password')
        }
        for i in range(len(list_portals)):
            if list_portals[i].get('name') == request.POST.get('portals'):
                portal = list_portals[i]

        portal_form = PortalForm(request.POST or None)
        if portal_form.is_valid():
            create_new_portal = portal_form.save(commit=False)
            if Portal.objects.filter(name=create_new_portal.name):
                messages.error(request, "Портал %s уже существует в вашем списке!" % portal['name'])
            else:
                # Auth user in selected portal and create portal in database 
                auth_portal_complate = auth_portal(portal, log_pass, request)
                if auth_portal_complate == True:
                    user = auth.get_user(request).username
                    create_new_portal.user = user
                    create_new_portal.save()
        return redirect('/main/')    

def delete_portal(request, id_portal):
    portal = Portal.objects.filter(pk=id_portal)
    portal.delete()
    return redirect('/main/')
