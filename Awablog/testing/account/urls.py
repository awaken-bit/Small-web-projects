from . import views
from django.urls import path, include
import django


urlpatterns = [
    # post views
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),

]
