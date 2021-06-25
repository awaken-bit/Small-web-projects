from . import views
from django.urls import path, include
import django


urlpatterns = [
    # post views
    path('profile/<slug:slug>',views.dashboard, name='dashboard'),
    path('settings', views.profile_settings, name='profile_settings'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),

]
