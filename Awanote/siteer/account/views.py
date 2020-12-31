from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm




def dashboard(request):
    return render(request, 'account/dashboard.html', {})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('news_home')
                else:
                    return render(request, 'account/messeng.html', {'mes': '<h1>Disabled account</h1>'})
            else:
                return render(request, 'account/messeng.html', {'mes': '<h1>Invalid login</h1>'})
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
