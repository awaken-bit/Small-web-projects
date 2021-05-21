from . import views
from django.urls import path, include
import django
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # post views
    path('',views.dashboard,name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),

]
