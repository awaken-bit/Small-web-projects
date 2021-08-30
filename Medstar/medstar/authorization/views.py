from main.models import Doctor, Hospital
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from .models import *
from django.db import connection, reset_queries
import time
import functools
from django.contrib.auth import authenticate, login, logout


# Other
def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result
    return inner_func

def user_logout(request):
    logout(request)
    return redirect('main')

def user_login(request):
    if request.method == 'POST' and request.user.is_anonymous:
        speks = request.POST
        try:
            speks['login']
            speks['password']
        except:
            raise Http404('Ошибка в данных')
        print(speks)
        authenticate_user = authenticate(username=speks.get('login'), password=speks.get('password'))
        if authenticate_user is not None:
            if authenticate_user.is_active:
                login(request, authenticate_user)
            else:
                raise Http404('Отключенная учетная запись')
        else:
            raise Http404('Неверный логин или пароль')

        return redirect('main')
    else:
        raise Http404

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'authorization/profile.html')
    else:
        raise Http404

def user_registration(request):
    if request.method == 'POST' and request.user.is_anonymous:
        speks = request.POST
        print(speks)
        try:
            speks['first_name']
            speks['last_name']
            speks['password']
            speks['title']
            speks['patronymic']
            speks['phone']
        except:
            raise Http404('Ошибка в данных')

        user = User(
            first_name = speks.get('first_name'),
            last_name = speks.get('last_name'),
        )
        user.set_password(speks.get('password'))
        user.save()
        user.username = user.id
        user.save()
        
        hospital = Hospital(
            title = speks.get('title')
        )
        hospital.save()
        
        doctor = Doctor(
            user = user,
            patronymic = speks.get('patronymic'),
            is_director = True,
            hospital = hospital,
            position = 'Главврач',
            password = speks.get('password'),
            phone_numder = speks.get('phone'),
            on_vacation = False,
            department = None
        )
        doctor.save()

        authenticate_user = authenticate(username=user.username, password=speks.get('password'))
        if authenticate_user is not None:
            if authenticate_user.is_active:
                login(request, authenticate_user)
            else:
                raise Http404('Отключенная учетная запись')
        else:
            raise Http404('Неверный логин')

        return redirect('main')
    else:
        raise Http404



