from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def registerUser(request):
    form = UserCreationForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            newuser = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth.login(request, newuser)
            return redirect('/account/login/')
    return render(request, 'register.html', context)

def authorizationUser(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(username=login, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/main/')
        else:
            return redirect('/account/login/')
    return render(request, 'login.html')

def logoutUser(request):
    auth.logout(request)
    return redirect('/main/')