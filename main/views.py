from django.shortcuts import render, redirect
from portal.handler import send_spam
from portal.forms import PortalForm
from portal.models import Portal
from django.contrib import auth


# Create your views here.
def main(request):
    if request.user.is_authenticated():
        portal_form = PortalForm()
        portals = Portal.objects.filter(user=auth.get_user(request).username)
        context = {
            'portal_form': portal_form,
            'portals': portals,
            'user': auth.get_user(request).username
        }
        if request.method == 'POST':
            portal_form = PortalForm(request.POST or None)
            if request.POST.get('title') == '' and request.POST.get('url') == '':
                context = {
                    'empty': 'Это поле обязательное!'
                }
            else:        
                if len(request.POST.get('title')) < 5 or len(request.POST.get('title')) > 50:
                    context = {
                        'length': 'Заголовок должен быть более 5 и менее 50 символов!'
                    }
                else:
                    # portals = []
                    # for portal in range(len(request.POST.get('den'))):
                    #     portals.append(request.POST.getlist('den')[portal])
                    input_data = {
                        'title': request.POST.get('title'),
                        'url': request.POST.get('url'),
                        'description': request.POST.get('description')
                    }
                    context = {
                        'portal_form': portal_form
                    }
                    print(request.POST.getlist('den'))

                    # Send spam
                    # send_spam(input_data, portals)
                    return redirect('/main/')
        return render(request, 'main.html', context)
    else:
        return redirect('/account/login/')
        
