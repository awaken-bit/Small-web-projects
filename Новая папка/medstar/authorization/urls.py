from django.urls import path
from .views import *


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/',profile, name='profile'),
    path('registration/', user_registration, name='registration')
]