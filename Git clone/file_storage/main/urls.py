
from os import name
from django.urls import path
from . import views 

urlpatterns = [
    path('repository/<int:pk>', views.get_repository, name='repository_view'),
    path('folder/<int:pk>', views.get_folder, name='folder_view'),
    path('file/<int:pk>', views.get_file, name='file_fiew'),
    
    path('download_repository/<int:pk>', views.download_repository, name='download_repository'),
    path('download_folder/<int:pk>', views.download_folder, name='download_folder'),
    
    path('delete_file/<int:pk>', views.delete_file, name='delete_file'),
    path('delete_folder/<int:pk>', views.delete_folder, name='delete_folder'),
    path('delete_repository/<int:pk>', views.delete_repository, name='delete_repository'),
    
    path('create_repository/', views.create_repository, name='create_repository'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('create_file/', views.create_file, name='create_file'),
    
    path('folder/<int:pk>/settings', views.folder_settings, name='folder_settings'),
    path('repository/<int:pk>/settings', views.repository_settings, name='repository_settings'),
    
    path('edit_file/<int:pk>', views.edit_file, name='edit_file'),
    
    path('image/<int:pk>', views.get_image, name='get_image'),
    path('', views.main, name='main'),
    path('follow/<slug:slug>', views.follow, name='follow'),
    path('search/', views.search_repositorys, name='search_repositorys')
]