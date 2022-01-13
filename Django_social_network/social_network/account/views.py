from main.models import Profile, User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

from django.core.files.storage import FileSystemStorage


def dashboard(request):
    user = request.user
    if user.is_authenticated:
        try:
            profile = Profile.objects.get(owner=user)
        except:
            profile = Profile(
                owner=user,
            )
            profile.save()
            return redirect('dashboard')
        if request.method == 'POST':
            if 'user_img' in request.FILES:
                file = request.FILES['user_img']
                extensions = ['png', 'jpg', 'jpeg']
                if file.name.split('.')[1] in extensions:
                    profile.image = file
                    profile.save()
            if request.POST['first_name'] != request.user.first_name:
                request.user.first_name = request.POST['first_name']
                request.user.save()
            if request.POST['last_name'] != request.user.last_name:
                request.user.last_name = request.POST['last_name']
                request.user.save()
            if request.POST['bio'] != profile.bio:
                profile.bio = request.POST['bio']
                profile.save()
                
            return redirect('dashboard')
        else:
            
            data = {
                'profile': profile,
            }
            return render(request, 'account/dashboard.html', data)
    else:
        return redirect('login')
    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home_non_auth')
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

def create_new_profiles_gogle(*args, **kwargs):
    if kwargs['is_new']:
        Profile.objects.create(
            owner = User.objects.get(username = kwargs['username'])
        )
