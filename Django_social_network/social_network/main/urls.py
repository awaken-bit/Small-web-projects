from django.urls import path
from . import views


urlpatterns = [
    path('user/<int:pk>', views.index, name='home'),
    path('', views.home, name='home_non_auth'),

    path('friends/', views.friends_list, name='friends_list'),
    path('groups/', views.messanges_groups_list, name='groups_list'),
    path('messanges/', views.messanges_friends_list,name='messanges_friends_list'),

    path('delete_friend/<int:pk>', views.delete_friend, name='delete_friend'),
    path('append_friend/<int:pk>', views.append_friend, name='append_friend'),

    path('delete_group/<int:pk>', views.delete_group, name='delete_group'),
    path('append_group/<int:pk>', views.append_group, name='append_group'),
    path('create_group/', views.create_group, name='create_group'),
    path('settings_group/<int:pk>', views.group_settings, name='settings_group'),


    path('chat/<int:pk>', views.chat, name='messanges'),
    path('chat_group/<int:pk>', views.chat_group, name='group_chat'),

]
