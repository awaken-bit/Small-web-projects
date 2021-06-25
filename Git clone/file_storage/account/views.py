from django.http import Http404
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from main import models
import datetime
from main.views import timedelta_to_dhms


def dashboard(request, slug):
    profile = models.Profile.objects.get(slug=slug)
    repositorys = []
    for i in profile.repository_set.all():
        time = datetime.datetime.today() - datetime.datetime(
                        i.changed_at.year, i.changed_at.month  ,i.changed_at.day, i.changed_at.hour, i.changed_at.minute)
        time = timedelta_to_dhms(time)
        repositorys.append([i, time])

    data = {
        'profile': profile,
        'repositorys': repositorys,
        'messeng': False
    }
    return render(request, 'account/dashboard.html', data)

def profile_settings(request):
    if request.user.is_authenticated:
        data = {
            'messeng': False
        }
        if request.method == 'POST':
            speks = request.POST
            files = request.FILES
            user = request.user
            if speks['what_it'] == 'change_password':
                user.set_password(speks['password'])
                user.save()
                authenticate_user = authenticate(username=user.username, password=speks['password'])
                login(request, authenticate_user)
                return redirect('profile_settings')
            elif speks['what_it'] == 'change_user_data':
                if speks['username'] != user.profile.slug:

                    try:
                        int(speks['username'])
                    except:
                        pass
                    else:
                        data['messeng'] = 'Имя пользователя должно содержать буквы.'
                        return render(request, 'account/profile_settings.html', data)

                    if models.Profile.objects.filter(slug=speks['username'])[:1]:
                        data['messeng'] = 'Пользователь с таким именем уже существует.'
                        return render(request, 'account/profile_settings.html', data)
                    else:
                        user.profile.slug = speks['username']
                if speks['first_name'] != user.first_name:
                    user.first_name = speks['first_name']
                if speks['last_name'] != user.last_name:
                    user.last_name = speks['last_name']
                if speks['bio'] != user.profile.bio:
                    user.profile.bio = speks['bio']
                if files:
                    if files.get('image') != user.profile.image and files.get('image').name.split('.')[-1] in ['png', 'jpeg', 'jpg']:
                        user.profile.image.delete()
                        user.profile.image = files.get('image')
                user.save()
                user.profile.save()
                return redirect('profile_settings')
            else:
                data['messeng'] = 'Ошибка в формате данных, попробуйте ещё раз.'
            
            return render(request, 'account/profile_settings.html', data)
        else:
            return render(request, 'account/profile_settings.html', data)
    else:
        raise Http404

def user_login(request):
    if request.method == 'POST':
        speks = request.POST
        user = authenticate(username=speks['username'], password=speks['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard', user.profile.slug)
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
