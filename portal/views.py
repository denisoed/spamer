from django.shortcuts import render, redirect
from .forms import PortalForm
from .list_portals import list_portals
from main.handler import register_user
from django.contrib import auth
from .models import Portal


# Create your views here.
def createPortal(request):
    if request.method == 'POST':
        log_pass = {
            'login': request.POST.get('login'),
            'password': request.POST.get('password')
        }
        for i in range(len(list_portals)):
            if list_portals[i].get('name') == request.POST.get('portals'):
                portal = list_portals[i]

        #Transfer settings for portals and user login/password
        register_user(portal, log_pass)  

        portal_form = PortalForm(request.POST or None)
        if portal_form.is_valid():
            add_author = portal_form.save(commit=False)
            user = auth.get_user(request).username
            if Portal.objects.filter(name=add_author.name):
                print('Уже есть')
            else:
                add_author.user = user
                add_author.save()    
        return redirect('/main/')
