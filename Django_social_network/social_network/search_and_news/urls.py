from django.urls import path
from . import views

urlpatterns = [
    path('friends/', views.search_friends, name='search_friends'),
    path('groups/', views.search_groups, name='search_groups'),
    path('news/', views.news_list, name='news_list'),
    path('popular_news/', views.popular_news_list, name='popular_news_list'),
    path('create_post/', views.create_post, name='create_post')

]