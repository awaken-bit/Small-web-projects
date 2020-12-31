from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update',views.NewsUpdateAR.as_view(), name='update'),
    path('<int:pk>/delete',views.NewsDeleteAR.as_view(), name='delete'),

]