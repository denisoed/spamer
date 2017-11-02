from django.shortcuts import render, redirect
from .forms import MainForms
from .handler import register_user


# Create your views here.
def main(request):
    form = MainForms()
    context = {
        'title': 'Main',
        'form': form,
    }
    
    if request.method == 'POST':
        portals = [
            request.POST.get('hackernews')
        ]
        data = {
            'title': request.POST.get('title'),
            'url': request.POST.get('url'),
            'description': request.POST.get('description')
        }
        # register_user(data)
        return redirect('/')
    return render(request, 'main.html', context)
